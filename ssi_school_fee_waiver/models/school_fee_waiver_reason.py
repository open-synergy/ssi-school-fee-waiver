# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolFeeWaiverReason(models.Model):
    """Represents the applicant-facing basis for a fee waiver request.

    A fee waiver reason records why a waiver is being requested (for
    example Economic Hardship, Orphan, Disaster, or Staff Family),
    independent of how the school classifies the waiver itself. This
    model only carries the reason; the waiver document that records
    which reason was used for a given request is added later by the
    transactional module.
    """

    _name = "school_fee_waiver_reason"
    _inherit = ["mixin.master_data"]
    _description = "School Fee Waiver Reason"
    _order = "sequence, name, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
        help="Display order of the fee waiver reason. Lower values "
        "appear first in the list.",
    )
