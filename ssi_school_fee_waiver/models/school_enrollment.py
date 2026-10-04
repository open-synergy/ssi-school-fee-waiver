# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolEnrollment(models.Model):
    # Extension of the enrollment: refuses cancellation while a fee
    # waiver billed against it is still active, and feeds the fee
    # waiver into the deduction hooks of the billing breakdown.
    _name = "school_enrollment"
    _inherit = [
        "school_enrollment",
    ]

    amount_fee_waiver_deducted = fields.Monetary(
        string="Fee Waiver Deducted",
        currency_field="currency_id",
        compute="_compute_amount_fee_waiver",
        store=True,
        compute_sudo=True,
        groups="ssi_school_fee_waiver.school_fee_waiver_viewer_group",
        help="Fee waiver already deducted from the invoices: the sum "
        "of Fee Waiver Deducted of the counted payment terms.",
    )
    amount_fee_waiver_undeducted = fields.Monetary(
        string="Fee Waiver Not Yet Deducted",
        currency_field="currency_id",
        compute="_compute_amount_fee_waiver",
        store=True,
        compute_sudo=True,
        groups="ssi_school_fee_waiver.school_fee_waiver_viewer_group",
        help="Fee waiver still waiting for deduction: the sum of Fee "
        "Waiver Not Yet Deducted of the counted payment terms.",
    )
    amount_fee_waiver = fields.Monetary(
        string="Fee Waiver Amount",
        currency_field="currency_id",
        compute="_compute_amount_fee_waiver",
        store=True,
        compute_sudo=True,
        groups="ssi_school_fee_waiver.school_fee_waiver_viewer_group",
        help="Effective fee waiver of this enrollment: Fee Waiver "
        "Deducted plus Fee Waiver Not Yet Deducted. The unrealized "
        "remainder of a partially deducted schedule is not counted, "
        "because it is billed to the student, so this amount can be "
        "lower than the sum of Fee Waiver Amount of the payment terms.",
    )

    @api.depends(
        "payment_term_ids.state",
        "payment_term_ids.fee_waiver_amount_deducted",
        "payment_term_ids.fee_waiver_amount_undeducted",
    )
    def _compute_amount_fee_waiver(self):
        """Summarize the fee waiver of the counted payment terms.

        Payment terms whose state is ``cancelled`` or ``voided`` are
        not counted, the same filter as ``amount_total``.

        :return: None
        """
        for record in self:
            amount_deducted = 0.0
            amount_undeducted = 0.0
            counted_terms = record.payment_term_ids.filtered(
                lambda term: term.state not in ("cancelled", "voided")
            )
            for term in counted_terms:
                amount_deducted += term.fee_waiver_amount_deducted
                amount_undeducted += term.fee_waiver_amount_undeducted
            record.amount_fee_waiver_deducted = amount_deducted
            record.amount_fee_waiver_undeducted = amount_undeducted
            record.amount_fee_waiver = amount_deducted + amount_undeducted

    def _get_amount_deduction(self):
        """Add the fee waiver to the total effective deduction.

        :return: Deduction of the base modules plus ``amount_fee_waiver``.
        :rtype: float
        """
        self.ensure_one()
        result = super()._get_amount_deduction()
        return result + self.amount_fee_waiver

    def _get_amount_deducted(self):
        """Add the deducted fee waiver to the deducted amount.

        :return: Deducted amount of the base modules plus
            ``amount_fee_waiver_deducted``.
        :rtype: float
        """
        self.ensure_one()
        result = super()._get_amount_deducted()
        return result + self.amount_fee_waiver_deducted

    @api.depends(
        "amount_fee_waiver",
        "amount_fee_waiver_deducted",
    )
    def _compute_amount_deduction(self):
        """Recompute the billing breakdown when the fee waiver changes.

        :return: None
        """
        super()._compute_amount_deduction()

    @ssi_decorator.pre_cancel_action()
    def _20_check_fee_waiver_active(self):
        """Reject cancelling an enrollment with an active fee waiver.

        A fee waiver is active while its state is neither ``cancel``
        nor ``reject``.

        :raises UserError: when an active fee waiver is billed
            against this enrollment.
        :return: None
        """
        self.ensure_one()
        waiver = (
            self.env["school_fee_waiver"]
            .sudo()
            .search(
                [
                    ("source_type", "=", "enrollment"),
                    ("enrollment_id", "=", self.id),
                    ("state", "not in", ["cancel", "reject"]),
                ],
                limit=1,
            )
        )
        if waiver:
            error_message = """
Document Type: %s
Context: Cancel enrollment
Database ID: %s
Problem: Enrollment has an active fee waiver '%s'
Solution: Cancel the fee waiver before cancelling this enrollment
""" % (
                self._description,
                self.id,
                waiver.display_name,
            )
            raise UserError(_(error_message))
