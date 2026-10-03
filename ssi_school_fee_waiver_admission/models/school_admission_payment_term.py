# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class SchoolAdmissionPaymentTerm(models.Model):
    # Extension of the admission payment term: refuses deleting a
    # term that a fee waiver or one of its Schedule lines refers to.
    _name = "school_admission_payment_term"
    _inherit = [
        "school_admission_payment_term",
    ]

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
