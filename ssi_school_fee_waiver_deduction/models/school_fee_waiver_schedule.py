# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolFeeWaiverSchedule(models.Model):
    """
    Extends the fee waiver schedule with a link back to the
    deduction document that realized it.

    Filled by ``school_fee_waiver_deduction``'s own
    ``_30_mark_schedule_realized`` hook when the deduction document
    opens, and cleared again by its ``_30_reset_schedule`` hook when
    the deduction document is cancelled.
    """

    _name = "school_fee_waiver_schedule"
    _inherit = [
        "school_fee_waiver_schedule",
    ]

    deduction_id = fields.Many2one(
        string="Deduction",
        comodel_name="school_fee_waiver_deduction",
        ondelete="set null",
        readonly=True,
        copy=False,
        help="Deduction document that realized this schedule line, " "if any.",
    )
