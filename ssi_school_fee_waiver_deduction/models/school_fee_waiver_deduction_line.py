# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolFeeWaiverDeductionLine(models.Model):
    """
    Represents one debit line of a fee waiver deduction document.

    A line realizes exactly one Schedule line of the linked Waiver:
    ``amount`` is the portion of that Schedule line's own Amount
    Planned actually being deducted now, posted to a discount/
    contra-revenue ``account_id``. This line's own ``account.move.line``
    is created by ``_create_standard_ml`` (``mixin.account_move_single_line``)
    as part of the header's ``_10_create_accounting_entry`` hook.
    """

    _name = "school_fee_waiver_deduction_line"
    _inherit = [
        "mixin.account_move_single_line",
    ]
    _description = "School Fee Waiver Deduction - Line"
    _order = "deduction_id, id"

    # Accounting Move Single Line Mixin (``mixin.account_move_single_line``)
    _move_id_field_name = "move_id"
    _account_id_field_name = "account_id"
    _analytic_account_id_field_name = "analytic_account_id"
    _amount_currency_field_name = "amount"
    _date_field_name = "date"
    _normal_amount = "debit"

    deduction_id = fields.Many2one(
        string="# Deduction",
        comodel_name="school_fee_waiver_deduction",
        required=True,
        ondelete="cascade",
        help="Deduction document this line belongs to.",
    )
    schedule_id = fields.Many2one(
        string="Schedule",
        comodel_name="school_fee_waiver_schedule",
        required=True,
        ondelete="restrict",
        help="Waiver Schedule line this deduction line realizes.",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=True,
        ondelete="restrict",
        help="Discount/contra-revenue account this line debits. "
        "Defaulted from the Schedule's own Waiver Type.",
    )
    amount = fields.Monetary(
        string="Amount",
        currency_field="currency_id",
        required=True,
        help="Portion of the Schedule line's own Amount Planned being "
        "deducted now. May not exceed the Schedule line's remaining "
        "planned amount.",
    )
    move_line_id = fields.Many2one(
        string="Journal Item",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
        help="Journal item created for this line once the parent "
        "document is opened.",
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        ondelete="restrict",
        help="Analytic account this line's journal item is posted " "against, if any.",
    )

    # Convenience fields mirrored from the header, following the
    # pattern of ``customer_invoice.line``.
    move_id = fields.Many2one(
        related="deduction_id.move_id",
        compute_sudo=True,
    )
    date = fields.Date(
        related="deduction_id.date",
        compute_sudo=True,
    )
    currency_id = fields.Many2one(
        related="deduction_id.currency_id",
        compute_sudo=True,
    )
    company_id = fields.Many2one(
        related="deduction_id.company_id",
        compute_sudo=True,
    )
    company_currency_id = fields.Many2one(
        related="deduction_id.company_currency_id",
        compute_sudo=True,
    )

    @api.onchange("schedule_id")
    def onchange_account_id(self):
        """Default Account from the Schedule's own Waiver Type.

        :return: nothing
        """
        self.account_id = False
        if self.schedule_id:
            self.account_id = self.schedule_id.waiver_id.type_id.discount_account_id

    @api.constrains("schedule_id", "amount")
    def _check_amount_not_exceed_remaining_planned(self):
        """Forbid deducting more than the Schedule line's remaining plan.

        :raises ValidationError: when ``amount`` exceeds the Schedule
            line's own Amount Planned minus its Amount Realized.
        """
        for record in self:
            schedule = record.schedule_id
            remaining = schedule.amount_planned - schedule.amount_realized
            if record.amount > remaining:
                error_message = """
Document Type: %s
Context: Configure deduction line
Database ID: %s
Problem: Amount %s exceeds Schedule line's remaining planned amount %s
Solution: Lower the Amount, or select a Schedule line with more remaining plan
""" % (
                    record._description,
                    record.id,
                    record.amount,
                    remaining,
                )
                raise ValidationError(_(error_message))

    @api.constrains("schedule_id")
    def _check_schedule_state(self):
        """Forbid a Schedule line already Realized, Skipped, or Cancelled.

        :raises ValidationError: when ``schedule_id.state`` is one of
            ``realized``, ``skipped``, or ``cancelled``.
        """
        for record in self:
            if record.schedule_id.state in ("realized", "skipped", "cancelled"):
                error_message = """
Document Type: %s
Context: Configure deduction line
Database ID: %s
Problem: Schedule line is in state '%s'
Solution: Select a Schedule line that is still Draft or Scheduled
""" % (
                    record._description,
                    record.id,
                    record.schedule_id.state,
                )
                raise ValidationError(_(error_message))

    @api.constrains("schedule_id", "deduction_id")
    def _check_schedule_belongs_to_waiver(self):
        """Require the Schedule line to belong to the document's Waiver.

        :raises ValidationError: when ``schedule_id.waiver_id`` differs
            from ``deduction_id.waiver_id``.
        """
        for record in self:
            if (
                record.schedule_id
                and record.deduction_id.waiver_id
                and record.schedule_id.waiver_id != record.deduction_id.waiver_id
            ):
                error_message = """
Document Type: %s
Context: Configure deduction line
Database ID: %s
Problem: Schedule line '%s' does not belong to this document's Waiver
Solution: Select a Schedule line that belongs to this document's own Waiver
""" % (
                    record._description,
                    record.id,
                    record.schedule_id.display_name,
                )
                raise ValidationError(_(error_message))

    @api.constrains("schedule_id", "deduction_id")
    def _check_duplicate_schedule(self):
        """Forbid the same Schedule line appearing twice on one document.

        :raises ValidationError: when another line of the same
            document already targets the same Schedule line.
        """
        for record in self:
            duplicate_count = self.search_count(
                [
                    ("id", "!=", record.id),
                    ("deduction_id", "=", record.deduction_id.id),
                    ("schedule_id", "=", record.schedule_id.id),
                ]
            )
            if duplicate_count > 0:
                error_message = """
Document Type: %s
Context: Configure deduction line
Database ID: %s
Problem: Schedule line '%s' is already used on another line of this document
Solution: Select a Schedule line not yet used on this document, or remove the duplicate line
""" % (
                    record._description,
                    record.id,
                    record.schedule_id.display_name,
                )
                raise ValidationError(_(error_message))

    def _get_standard_label(self):
        """Build the journal item label from the document and schedule.

        There is no ``name``/description field on this line by
        design, so the label is composed from the parent document's
        own number and the realized Schedule line's display name.

        :return: the composed label string
        """
        self.ensure_one()
        return "%s - %s" % (self.deduction_id.name, self.schedule_id.display_name)
