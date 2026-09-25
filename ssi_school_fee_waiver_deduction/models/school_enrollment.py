# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class SchoolEnrollment(models.Model):
    _name = "school_enrollment"
    _inherit = [
        "school_enrollment",
    ]

    def _check_revenue_recognition_readiness(self):
        """Extend the base readiness check with the fee waiver check.

        :raises UserError: from either the base check or
            ``_check_fee_waiver_deduction_readiness``
        :return: None
        """
        super()._check_revenue_recognition_readiness()
        self._check_fee_waiver_deduction_readiness()

    def _check_fee_waiver_deduction_readiness(self):
        """Reject finishing while a fee waiver deduction is still pending.

        Extension point of ``_check_revenue_recognition_readiness``.
        Rejects any ``school_fee_waiver_deduction`` still
        ``draft``/``confirm`` with an Allocation pointing to one of
        this enrollment's own invoiced payment terms -- such a
        deduction has not booked its own accounting entry yet, so it
        cannot be reclassed by this enrollment's own Revenue
        Recognition. Confirmed by the user: a pending deduction always
        blocks ``done``, whether or not it would end up deferred once
        opened.

        :raises UserError: when a matching deduction is still
            ``draft``/``confirm``
        :return: None
        """
        self.ensure_one()
        invoice_ids = self.payment_term_ids.mapped("customer_invoice_id").ids
        if not invoice_ids:
            return
        pending = self.env["school_fee_waiver_deduction"].search(
            [
                ("state", "in", ("draft", "confirm")),
                ("allocation_ids.customer_invoice_id", "in", invoice_ids),
            ]
        )
        if pending:
            error_message = (
                _(
                    """
Context: Finish enrollment
Database ID: %s
Problem: Fee waiver deduction '%s' allocated to this enrollment's own \
invoice is still Draft/Waiting for Approval
Solution: Confirm and open that deduction before finishing this enrollment
"""
                )
                % (self.id, pending[0].display_name)
            )
            raise UserError(error_message)

    def _prepare_revenue_recognition_line_data(self):
        """Extend the base line list with the fee waiver deduction lines.

        :return: list of dict of
            ``school_enrollment_revenue_recognition_line`` values
        """
        result = super()._prepare_revenue_recognition_line_data()
        result += self._prepare_fee_waiver_deduction_recognition_line_data()
        return result

    def _prepare_fee_waiver_deduction_recognition_line_data(self):
        """Build the Recognition Line values for deferred deductions.

        Extension point of ``_prepare_revenue_recognition_line_data``.
        One line per Line of every ``open`` fee waiver deduction whose
        ``recognition_method`` is ``enrollment`` and that has at least
        one Allocation pointing to one of this enrollment's own
        invoiced payment terms. The amount reclassed is that Line's
        own ``amount`` scaled by this deduction's own share allocated
        to this enrollment (Σ of this deduction's own Allocations
        pointing to this enrollment's invoices, divided by the
        deduction's own ``amount_total``), negated so the mixin swaps
        the usual debit/credit sides: the Deferred Discount Account
        (this Line's current ``account_id``) ends up credited, and the
        Line's own Final Account ends up debited.

        :return: list of dict of
            ``school_enrollment_revenue_recognition_line`` values
        """
        self.ensure_one()
        result = []
        invoice_ids = self.payment_term_ids.mapped("customer_invoice_id").ids
        if not invoice_ids:
            return result
        deductions = self.env["school_fee_waiver_deduction"].search(
            [
                ("state", "=", "open"),
                ("recognition_method", "=", "enrollment"),
                ("allocation_ids.customer_invoice_id", "in", invoice_ids),
            ]
        )
        for deduction in deductions:
            if not deduction.amount_total:
                continue
            own_allocations = deduction.allocation_ids.filtered(
                lambda allocation: allocation.customer_invoice_id.id in invoice_ids
            )
            ratio = sum(own_allocations.mapped("amount")) / deduction.amount_total
            for line in deduction.line_ids:
                amount = deduction.currency_id.round(-1 * line.amount * ratio)
                # pylint: disable=protected-access
                label = line._get_standard_label()
                result.append(
                    {
                        "enrollment_id": self.id,
                        "name": label,
                        "fee_waiver_deduction_line_id": line.id,
                        "debit_account_id": line.account_id.id,
                        "credit_account_id": line.final_account_id.id,
                        "analytic_account_id": line.analytic_account_id.id,
                        "partner_id": deduction.partner_id.id,
                        "amount": amount,
                    }
                )
        return result
