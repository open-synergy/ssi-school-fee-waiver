# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SchoolAdmissionPaymentTerm(models.Model):
    # Extension of the admission payment term: refuses deleting a
    # term that a fee waiver or one of its Schedule lines refers to.
    _name = "school_admission_payment_term"
    _inherit = [
        "school_admission_payment_term",
    ]

    fee_waiver_schedule_ids = fields.One2many(
        string="Fee Waiver Schedules",
        comodel_name="school_fee_waiver_schedule",
        inverse_name="admission_payment_term_id",
        readonly=True,
        help="Fee waiver schedule lines that target this payment term.",
    )
    fee_waiver_amount = fields.Monetary(
        string="Fee Waiver Amount",
        currency_field="currency_id",
        compute="_compute_fee_waiver_amount",
        store=True,
        compute_sudo=True,
        help="Total fee waiver given to this payment term: the sum of "
        "Amount Planned of Scheduled and Realized schedule lines whose "
        "waiver is Running or Finished.",
    )
    fee_waiver_amount_deducted = fields.Monetary(
        string="Fee Waiver Deducted",
        currency_field="currency_id",
        compute="_compute_fee_waiver_amount",
        store=True,
        compute_sudo=True,
        help="Fee waiver already deducted: the sum of Amount Realized "
        "of Realized schedule lines.",
    )
    fee_waiver_amount_deducted_planned = fields.Monetary(
        string="Fee Waiver Deducted (Planned)",
        currency_field="currency_id",
        compute="_compute_fee_waiver_amount",
        store=True,
        compute_sudo=True,
        help="Planned amount of the fee waiver already deducted: the "
        "sum of Amount Planned of Realized schedule lines. It can "
        "exceed the actual deducted amount on a partial deduction.",
    )
    fee_waiver_amount_undeducted = fields.Monetary(
        string="Fee Waiver Not Yet Deducted",
        currency_field="currency_id",
        compute="_compute_fee_waiver_amount",
        store=True,
        compute_sudo=True,
        help="Fee waiver still waiting for deduction: the sum of "
        "Amount Planned of Scheduled schedule lines whose waiver is "
        "Running or Finished.",
    )

    @api.depends(
        "fee_waiver_schedule_ids.state",
        "fee_waiver_schedule_ids.amount_planned",
        "fee_waiver_schedule_ids.amount_realized",
        "fee_waiver_schedule_ids.waiver_id.state",
    )
    def _compute_fee_waiver_amount(self):
        """Summarize the fee waiver schedules of each payment term.

        Only schedule lines whose waiver is ``open`` or ``done``
        count. Draft, Skipped and Cancelled schedule lines are
        ignored; the unrealized remainder of a partial deduction is
        not counted as not yet deducted, since a Realized line can
        not be deducted again.

        :return: nothing; assigns the four ``fee_waiver_amount*``
            fields
        """
        for record in self:
            total = 0.0
            deducted = 0.0
            deducted_planned = 0.0
            undeducted = 0.0
            for schedule in record.fee_waiver_schedule_ids:
                if schedule.waiver_id.state not in ("open", "done"):
                    continue
                if schedule.state == "scheduled":
                    total += schedule.amount_planned
                    undeducted += schedule.amount_planned
                elif schedule.state == "realized":
                    total += schedule.amount_planned
                    deducted += schedule.amount_realized
                    deducted_planned += schedule.amount_planned
            record.fee_waiver_amount = total
            record.fee_waiver_amount_deducted = deducted
            record.fee_waiver_amount_deducted_planned = deducted_planned
            record.fee_waiver_amount_undeducted = undeducted

    def _check_fee_waiver_reference(self):
        """Reject deleting a payment term referred to by a fee waiver.

        Looks for a fee waiver whose ``admission_payment_term_id`` is
        one of these terms, or a Schedule line pinned to one of them.
        The state of the waiver does not matter: the database foreign
        keys are ``restrict`` regardless of state.

        :raises UserError: naming the first referring waiver and the
            payment term it refers to.
        :return: None
        """
        if not self.ids:
            return
        waiver_model = self.env["school_fee_waiver"].sudo()
        schedule_model = self.env["school_fee_waiver_schedule"].sudo()
        waiver = waiver_model.search(
            [("admission_payment_term_id", "in", self.ids)],
            limit=1,
        )
        term = waiver.admission_payment_term_id
        if not waiver:
            schedule = schedule_model.search(
                [("admission_payment_term_id", "in", self.ids)],
                limit=1,
            )
            waiver = schedule.waiver_id
            term = schedule.admission_payment_term_id
        if waiver:
            error_message = """
Document Type: %s
Context: Delete admission payment term
Database ID: %s
Problem: Payment term '%s' is referenced by fee waiver '%s'
Solution: Cancel the fee waiver before deleting its payment terms
""" % (
                self._description,
                term.id,
                term.display_name,
                waiver.display_name,
            )
            raise UserError(_(error_message))

    def unlink(self):
        """Refuse deleting payment terms referred to by a fee waiver.

        Guarding ``unlink`` (rather than the Compute Payment button)
        covers Compute Payment, the Copy Payment Term wizard, and
        manual deletion of a row in a single place.

        :raises UserError: when a fee waiver refers to a deleted term.
        :return: ``True``
        """
        self._check_fee_waiver_reference()
        return super().unlink()
