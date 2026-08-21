# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolFeeWaiverType(models.Model):
    """
    Extends the fee waiver type with the accounting configuration a
    deduction document of this type defaults its own Journal and
    Line Account from.

    Kept on the type rather than on each deduction document, so the
    accounting policy is set once per fee waiver type instead of
    being re-entered on every document.
    """

    _name = "school_fee_waiver_type"
    _inherit = [
        "school_fee_waiver_type",
    ]

    deduction_journal_id = fields.Many2one(
        string="Deduction Journal",
        comodel_name="account.journal",
        ondelete="restrict",
        help="Accounting journal a deduction document of this fee "
        "waiver type defaults its own Journal from.",
    )
    discount_account_id = fields.Many2one(
        string="Discount Account",
        comodel_name="account.account",
        ondelete="restrict",
        help="Discount/contra-revenue account a deduction line of "
        "this fee waiver type defaults its own Account from.",
    )
