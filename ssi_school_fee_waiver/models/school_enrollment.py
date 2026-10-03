# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolEnrollment(models.Model):
    # Extension of the enrollment: refuses cancellation while a fee
    # waiver billed against it is still active.
    _name = "school_enrollment"
    _inherit = [
        "school_enrollment",
    ]

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
