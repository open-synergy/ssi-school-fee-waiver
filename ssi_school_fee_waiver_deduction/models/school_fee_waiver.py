# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class SchoolFeeWaiver(models.Model):
    """
    Guards schedule regeneration against stale Schedule lines still
    referenced by a Deduction line.

    ``school_fee_waiver_deduction_line.schedule_id`` carries
    ``ondelete="restrict"`` back to ``school_fee_waiver_schedule``.
    The parent's ``_generate_schedule`` unconditionally unlinks every
    stale (``draft``/``scheduled``) Schedule line, so without this
    guard it would raise a raw ``IntegrityError`` the moment a
    Deduction line still points at one of them. This override turns
    that into a readable ``UserError`` instead, raised before the
    unlink is ever attempted.
    """

    _name = "school_fee_waiver"
    _inherit = [
        "school_fee_waiver",
    ]

    def _generate_schedule(self, bypass_policy_check=False):
        """Reject regeneration while a stale line is still referenced.

        :param bypass_policy_check: forwarded to ``super()`` unchanged
        :raises UserError: when a Schedule line about to be deleted
            (state ``draft``/``scheduled``) is still referenced by a
            ``school_fee_waiver_deduction_line``
        :return: nothing; delegates to ``super()`` once the guard
            passes
        """
        self.ensure_one()
        stale = self.schedule_ids.filtered(
            lambda schedule: schedule.state in ("draft", "scheduled")
        )
        deduction_line_obj = self.env["school_fee_waiver_deduction_line"]
        referenced = deduction_line_obj.search([("schedule_id", "in", stale.ids)])
        if referenced:
            error_message = """
Document Type: %s
Context: Regenerate waiver schedule
Database ID: %s
Problem: Schedule line(s) %s about to be regenerated are still \
referenced by a Deduction line
Solution: Cancel or reallocate the Deduction line(s) referencing \
those Schedule line(s) first
""" % (
                self._description,
                self.id,
                ", ".join(referenced.mapped("schedule_id.display_name")),
            )
            raise UserError(_(error_message))
        return super()._generate_schedule(bypass_policy_check=bypass_policy_check)
