# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolFeeWaiverReason(models.Model):  # pylint: disable=too-few-public-methods
    """Extend School Fee Waiver Reason with single operating unit support.

    Restricts each fee waiver reason record to one operating unit, for
    operating unit-based data segregation. Unlike
    ``school_fee_waiver``, no derivation is registered here -- the
    field simply defaults to the creating user's own operating unit,
    same as ``mixin.single_operating_unit`` provides out of the box.
    """

    _name = "school_fee_waiver_reason"
    _inherit = [
        "school_fee_waiver_reason",
        "mixin.single_operating_unit",
    ]
