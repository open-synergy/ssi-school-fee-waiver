# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolFeeWaiverSchedule(models.Model):
    """Extend Schedule with an Admission Payment Term source field.

    Gives a Schedule line a second, mutually-exclusive source term
    field, ``admission_payment_term_id``, alongside the base module's
    ``payment_term_id`` (an enrollment payment term). All
    ``_get_source_term*`` hooks fall back to ``super()`` whenever
    ``admission_payment_term_id`` is empty, so enrollment-sourced
    Schedule lines keep working unmodified.
    """

    _name = "school_fee_waiver_schedule"
    _inherit = [
        "school_fee_waiver_schedule",
    ]

    admission_payment_term_id = fields.Many2one(
        string="Admission Payment Term",
        comodel_name="school_admission_payment_term",
        ondelete="restrict",
        help="Admission payment term this Schedule line realizes. Set "
        "instead of Payment Term when this line was generated from an "
        "Admission-sourced waiver.",
    )

    def _get_source_term(self):
        """Return the Admission payment term when one is set.

        :return: ``admission_payment_term_id`` when set, otherwise
            whatever ``super()`` returns
        """
        self.ensure_one()
        if self.admission_payment_term_id:
            return self.admission_payment_term_id
        return super()._get_source_term()

    def _get_source_term_parent(self):
        """Return the Admission owning the source term when one is set.

        :return: the Admission payment term's own ``admission_id``
            when set, otherwise whatever ``super()`` returns
        """
        self.ensure_one()
        if self.admission_payment_term_id:
            return self.admission_payment_term_id.admission_id
        return super()._get_source_term_parent()

    @api.depends(
        "payment_term_id",
        "payment_term_id.detail_ids.price_subtotal",
        "payment_term_id.detail_ids.product_id",
        "payment_term_id.detail_ids.product_id.categ_id",
        "admission_payment_term_id",
        "admission_payment_term_id.detail_ids.price_subtotal",
        "admission_payment_term_id.detail_ids.product_id",
        "admission_payment_term_id.detail_ids.product_id.categ_id",
        "line_id.product_id",
        "line_id.product_category_id",
    )
    def _compute_base_amount(self):
        """Widen the Base Amount computation's dependencies.

        Odoo does not merge ``@api.depends`` across an inherited
        method's redefinitions -- only the decorator on the final
        method in the MRO takes effect -- so
        ``admission_payment_term_id`` and its detail lines must be
        declared here for a change to them to retrigger this compute.
        The body itself is unchanged: ``super()`` already goes
        through ``_get_source_term()``, which this module overrides
        to resolve ``admission_payment_term_id`` too.

        :return: whatever ``super()._compute_base_amount()`` returns
        """
        return super()._compute_base_amount()

    @api.constrains("payment_term_id", "admission_payment_term_id")
    def _check_single_source_term(self):
        """Require exactly one of Payment Term / Admission Payment Term.

        Both fields realize the same schedule line against a
        different billing source; leaving both set or both empty
        makes ``_get_source_term()`` ambiguous or empty.

        :raises ValidationError: when both are set, or neither is
            set.
        """
        for record in self:
            if bool(record.payment_term_id) == bool(record.admission_payment_term_id):
                error_message = """
Document Type: %s
Context: Configure waiver schedule
Database ID: %s
Problem: Exactly one of Payment Term or Admission Payment Term must be set
Solution: Select either a Payment Term or an Admission Payment Term, not both and not neither
""" % (
                    record._description,
                    record.id,
                )
                raise ValidationError(_(error_message))
