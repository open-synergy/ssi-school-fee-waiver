# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolFeeWaiverType(models.Model):
    """Represents a school-defined classification of fee waivers.

    A fee waiver type groups waivers by the school's own policy (for
    example a discretionary waiver versus a scholarship-linked
    waiver), independent of the applicant's reason for requesting
    one. This model only carries the classification itself; the
    accounting configuration a waiver document of this type posts to
    is added later by ``ssi_school_fee_waiver_deduction``.
    """

    _name = "school_fee_waiver_type"
    _inherit = ["mixin.master_data"]
    _description = "School Fee Waiver Type"
    _order = "sequence, name, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
        help="Display order of the fee waiver type. Lower values "
        "appear first in the list.",
    )
