# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolFeeWaiverDeductionAllocation(models.Model):
    """
    Represents one customer invoice a fee waiver deduction is
    reconciled against.

    An allocation line states how much of the deduction document's
    Amount Total (``amount``) is applied to a given open
    ``customer_invoice``, capped at that invoice's own residual. The
    header's ``_20_reconcile`` hook merges the invoice's own
    receivable journal item with the header's own
    ``receivable_move_line_id`` and calls ``reconcile()``, then
    snapshots the invoice's receivable journal item here as
    ``move_line_id`` for traceability.
    """

    _name = "school_fee_waiver_deduction_allocation"
    _description = "School Fee Waiver Deduction - Allocation"
    _order = "deduction_id, id"

    deduction_id = fields.Many2one(
        string="# Deduction",
        comodel_name="school_fee_waiver_deduction",
        required=True,
        ondelete="cascade",
        help="Deduction document this allocation line belongs to.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="deduction_id.currency_id",
        store=True,
        compute_sudo=True,
        help="Currency of the parent document.",
    )
    customer_invoice_id = fields.Many2one(
        string="Customer Invoice",
        comodel_name="customer_invoice",
        required=True,
        ondelete="restrict",
        domain="[('partner_id', '=', parent.partner_id), "
        "('state', '=', 'open'), ('amount_residual', '>', 0)]",
        help="Open customer invoice this allocation reconciles "
        "against. Restricted to invoices of this document's own "
        "Partner with a positive residual.",
    )
    move_line_id = fields.Many2one(
        string="Invoice Receivable Move Line",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
        help="Receivable journal item of the selected invoice, "
        "reconciled against this document's own receivable journal "
        "item once this document is opened. Filled by the header's "
        "``_20_reconcile`` hook.",
    )
    amount = fields.Monetary(
        string="Amount",
        currency_field="currency_id",
        required=True,
        help="Portion of this document's Amount Total applied to the "
        "selected invoice. May not exceed the invoice's own residual.",
    )

    @api.constrains("amount", "customer_invoice_id")
    def _check_amount_not_exceed_residual(self):
        """Forbid allocating more than the invoice's own residual.

        :raises ValidationError: when ``amount`` exceeds the selected
            invoice's own ``amount_residual``.
        """
        for record in self:
            if (
                record.customer_invoice_id
                and record.amount > record.customer_invoice_id.amount_residual
            ):
                error_message = """
Document Type: %s
Context: Configure deduction allocation
Database ID: %s
Problem: Amount %s exceeds invoice '%s' residual %s
Solution: Lower the Amount to the invoice's own residual
""" % (
                    record._description,
                    record.id,
                    record.amount,
                    record.customer_invoice_id.display_name,
                    record.customer_invoice_id.amount_residual,
                )
                raise ValidationError(_(error_message))

    @api.constrains("customer_invoice_id", "deduction_id")
    def _check_partner_match(self):
        """Require the invoice's Partner to match the document's own.

        :raises ValidationError: when ``customer_invoice_id.partner_id``
            differs from ``deduction_id.partner_id``.
        """
        for record in self:
            if (
                record.customer_invoice_id
                and record.deduction_id.partner_id
                and record.customer_invoice_id.partner_id
                != record.deduction_id.partner_id
            ):
                error_message = """
Document Type: %s
Context: Configure deduction allocation
Database ID: %s
Problem: Invoice '%s' Partner does not match this document's Partner
Solution: Select an invoice billed to this document's own Partner
""" % (
                    record._description,
                    record.id,
                    record.customer_invoice_id.display_name,
                )
                raise ValidationError(_(error_message))

    @api.constrains("customer_invoice_id", "deduction_id")
    def _check_duplicate_customer_invoice(self):
        """Forbid the same invoice appearing twice on one document.

        :raises ValidationError: when another allocation line of the
            same deduction document already targets the same invoice.
        """
        for record in self:
            duplicate_count = self.search_count(
                [
                    ("id", "!=", record.id),
                    ("deduction_id", "=", record.deduction_id.id),
                    ("customer_invoice_id", "=", record.customer_invoice_id.id),
                ]
            )
            if duplicate_count > 0:
                error_message = """
Document Type: %s
Context: Configure deduction allocation
Database ID: %s
Problem: Invoice '%s' is already allocated on this document
Solution: Select an invoice not yet allocated on this document, or remove the duplicate line
""" % (
                    record._description,
                    record.id,
                    record.customer_invoice_id.display_name,
                )
                raise ValidationError(_(error_message))
