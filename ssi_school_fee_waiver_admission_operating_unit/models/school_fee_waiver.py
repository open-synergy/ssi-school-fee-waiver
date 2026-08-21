# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models

from odoo.addons.ssi_school_operating_unit.models.school_enrollment_operating_unit_mixin import (  # noqa: B950 pylint: disable=line-too-long
    get_operating_unit_id_from_school,
)


class SchoolFeeWaiver(models.Model):
    """Extend the Operating Unit derivation to the Admission source.

    ``ssi_school_fee_waiver_operating_unit`` only derives
    ``operating_unit_id`` from ``enrollment_id`` (via
    ``_derive_operating_unit_from_enrollment``, called from its own
    ``create``/``write`` overrides), so a waiver billed against an
    Admission (``source_type == "admission"``, added by
    ``ssi_school_fee_waiver_admission``) never carries
    ``enrollment_id`` in its ``create``/``write`` ``vals`` and falls
    back to the creating user's default operating unit from
    ``mixin.single_operating_unit`` instead of the Admission's own
    school's operating unit.

    Rather than writing a second, competing ``create``/``write``
    override -- two overrides that do not know about each other would
    clobber one another depending on ``depends`` load order -- this
    module extends the existing ``_derive_operating_unit_from_enrollment``
    hook itself with ``super()``, adding the missing Admission branch.
    The "exactly one operating unit" determination is delegated to the
    same ``get_operating_unit_id_from_school`` helper the existing
    adaptor already uses, so that rule is never duplicated.
    """

    _name = "school_fee_waiver"
    _inherit = [
        "school_fee_waiver",
    ]

    def _derive_operating_unit_from_enrollment(self, vals):
        """Also derive ``operating_unit_id`` from ``admission_id``.

        Calls ``super()`` first for the unchanged Enrollment path,
        then applies the same rule to ``admission_id``: only when
        ``admission_id`` is present in ``vals`` and the caller has
        not already supplied ``operating_unit_id`` in the same
        ``vals`` -- an explicit value always wins, and a school
        without exactly one operating unit leaves ``vals`` untouched
        without raising.

        :param vals: the ``create``/``write`` values dict, mutated in
            place
        :return: whatever ``super()`` returns (``None``)
        """
        result = super()._derive_operating_unit_from_enrollment(vals)
        if "admission_id" not in vals or "operating_unit_id" in vals:
            return result
        admission = self.env["school_admission"].browse(vals["admission_id"])
        operating_unit_id = get_operating_unit_id_from_school(
            self.env, admission.school_id.id
        )
        if operating_unit_id:
            vals["operating_unit_id"] = operating_unit_id
        return result
