# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolEnrollmentRevenueRecognitionLine(models.Model):
    _name = "school_enrollment_revenue_recognition_line"
    _inherit = [
        "school_enrollment_revenue_recognition_line",
    ]

    # Added by ``ssi_school_fee_waiver_deduction``: traces a
    # deduction-originated Recognition Line back to the fee waiver
    # deduction Line it reclasses, so cancelling that deduction can be
    # rejected once it has been recognized (``_05_check_not_recognized``).
    fee_waiver_deduction_line_id = fields.Many2one(
        string="Fee Waiver Deduction Line",
        comodel_name="school_fee_waiver_deduction_line",
        ondelete="restrict",
        help="Fee waiver deduction Line this Recognition Line "
        "reclasses from its Deferred Discount Account to its own "
        "Final Account. Empty for a Recognition Line originating "
        "from an invoiced payment term detail instead.",
    )
