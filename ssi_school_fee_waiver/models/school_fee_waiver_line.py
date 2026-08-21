# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolFeeWaiverLine(models.Model):
    """
    Represents one billing component a fee waiver covers.
    A line names its billing component either as a single Product or
    as a whole Product Category (never both, never neither), and how
    much of it is waived: a Percentage of the term's billed amount for
    that component, a Fixed Amount, or Full Coverage. ``Generate
    Schedule`` on the waiver expands each line into one Schedule line
    per matching payment term.
    """

    _name = "school_fee_waiver_line"
    _description = "School Fee Waiver Line"
    _order = "id"

    waiver_id = fields.Many2one(
        string="Waiver",
        comodel_name="school_fee_waiver",
        required=True,
        ondelete="cascade",
        help="Fee waiver this line belongs to.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="waiver_id.company_currency_id",
        store=True,
        compute_sudo=True,
        help="Currency Fixed Amount and Max Amount are expressed in, "
        "following the waiver's Company Currency.",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        ondelete="restrict",
        help="Product this line covers. Leave empty when this line "
        "covers a whole Product Category instead.",
    )
    product_category_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
        ondelete="restrict",
        help="Product category this line covers. Leave empty when "
        "this line covers a single Product instead.",
    )
    computation = fields.Selection(
        string="Computation",
        selection=[
            ("percentage", "Percentage"),
            ("fixed", "Fixed Amount"),
            ("full", "Full Coverage"),
        ],
        default="percentage",
        required=True,
        help="How the waived amount is computed: a percentage of the "
        "billed amount, a fixed amount, or full coverage.",
    )
    percentage = fields.Float(
        string="Percentage",
        digits=(5, 2),
        default=0.0,
        help="Percentage of the billed amount waived by this line. "
        "Only relevant when Computation is Percentage.",
    )
    amount_fixed = fields.Monetary(
        string="Fixed Amount",
        currency_field="currency_id",
        default=0.0,
        help="Fixed amount waived by this line. Only relevant when "
        "Computation is Fixed Amount.",
    )
    max_amount = fields.Monetary(
        string="Max Amount",
        currency_field="currency_id",
        default=0.0,
        help="Ceiling this line may waive in a single term. Zero "
        "means there is no ceiling.",
    )
    schedule_ids = fields.One2many(
        string="Schedule",
        comodel_name="school_fee_waiver_schedule",
        inverse_name="line_id",
        help="Schedule lines realizing this line, one per matching " "payment term.",
    )

    @api.constrains("product_id", "product_category_id")
    def _check_product_or_category(self):
        """Require exactly one of Product / Product Category.

        :raises ValidationError: when both are set, or neither is
            set.
        """
        for record in self:
            if bool(record.product_id) == bool(record.product_category_id):
                error_message = """
Document Type: %s
Context: Configure waiver line
Database ID: %s
Problem: Exactly one of Product or Product Category must be set
Solution: Select either a Product or a Product Category, not both and not neither
""" % (
                    record._description,
                    record.id,
                )
                raise ValidationError(_(error_message))

    @api.constrains("computation", "percentage")
    def _check_percentage(self):
        """Require a Percentage strictly between 0 and 100.

        :raises ValidationError: when Computation is Percentage and
            ``percentage`` is not in the open-closed range
            ``0 < percentage <= 100``.
        """
        for record in self:
            if record.computation == "percentage" and not (
                0 < record.percentage <= 100
            ):
                error_message = """
Document Type: %s
Context: Configure waiver line
Database ID: %s
Problem: Percentage %s is not between 0 (exclusive) and 100 (inclusive)
Solution: Enter a Percentage greater than 0 and up to 100
""" % (
                    record._description,
                    record.id,
                    record.percentage,
                )
                raise ValidationError(_(error_message))

    @api.constrains("computation", "amount_fixed")
    def _check_amount_fixed(self):
        """Require a positive Fixed Amount.

        :raises ValidationError: when Computation is Fixed Amount and
            ``amount_fixed`` is not above zero.
        """
        for record in self:
            if record.computation == "fixed" and record.amount_fixed <= 0:
                error_message = """
Document Type: %s
Context: Configure waiver line
Database ID: %s
Problem: Fixed Amount %s is not above zero
Solution: Enter a Fixed Amount greater than zero
""" % (
                    record._description,
                    record.id,
                    record.amount_fixed,
                )
                raise ValidationError(_(error_message))
