# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolFeeWaiver(models.Model):
    """Extend School Fee Waiver with an Admission billing source.

    Registers ``admission`` as a second ``source_type`` value,
    alongside the base module's ``enrollment``, so a fee waiver can
    also be billed against a ``school_admission`` -- for the case
    where a waiver is decided before the student is formally
    enrolled, once the admission itself has reached state Open (the
    point at which ``school_admission`` creates its own
    ``school_student_id``) but before an enrollment necessarily
    exists. All ``_get_source_*``/schedule hooks fall back to
    ``super()`` whenever ``source_type`` is not ``admission``, so
    enrollment-sourced waivers keep working unmodified.
    """

    _name = "school_fee_waiver"
    _inherit = [
        "school_fee_waiver",
    ]

    source_type = fields.Selection(
        selection_add=[
            ("admission", "Admission"),
        ],
        ondelete={"admission": "set default"},
    )
    admission_id = fields.Many2one(
        string="Admission",
        comodel_name="school_admission",
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Admission this waiver is billed against. Must already "
        "be linked to the selected Student's School Student record -- "
        "an admission earlier than Open has not yet created one, so "
        "it cannot be billed against. Required when Billing Source is "
        "Admission -- enforced by ``_check_billing_source``, not by "
        "this field itself, so the base module's own billing source "
        "is not forced to also be a required field.",
    )

    @api.depends("enrollment_id", "admission_id")
    def _compute_partner_id(self):
        """Derive Partner from the Admission's own Student too.

        Not a simple widen-and-forward like the other three computes
        below: ``school_admission`` has no ``partner_id`` field of
        its own (unlike ``school_enrollment``), so the base
        implementation's generic ``source.partner_id`` body cannot
        resolve an Admission-sourced waiver's Partner -- it would
        raise on a field that does not exist on ``school_admission``.
        This override branches on ``source_type`` instead: the
        non-Admission subset is still handled by ``super()``
        unchanged.

        :return: nothing; assigns ``partner_id``
        """
        admission_records = self.filtered(
            lambda record: record.source_type == "admission"
        )
        super(SchoolFeeWaiver, self - admission_records)._compute_partner_id()
        for record in admission_records:
            record.partner_id = (
                record.admission_id.student_id if record.admission_id else False
            )

    @api.depends("enrollment_id", "admission_id")
    def _compute_school_id(self):
        """Widen the School computation's dependencies to Admission.

        See ``_compute_partner_id`` for why this redeclaration is
        needed and why the body only forwards to ``super()``.

        :return: whatever ``super()._compute_school_id()`` returns
        """
        return super()._compute_school_id()

    @api.depends("enrollment_id", "admission_id")
    def _compute_grade_id(self):
        """Widen the Grade computation's dependencies to Admission.

        See ``_compute_partner_id`` for why this redeclaration is
        needed and why the body only forwards to ``super()``.

        :return: whatever ``super()._compute_grade_id()`` returns
        """
        return super()._compute_grade_id()

    @api.depends("enrollment_id", "admission_id")
    def _compute_academic_year_id(self):
        """Widen the Academic Year computation's dependencies.

        See ``_compute_partner_id`` for why this redeclaration is
        needed and why the body only forwards to ``super()``.

        :return: whatever ``super()._compute_academic_year_id()``
            returns
        """
        return super()._compute_academic_year_id()

    @api.constrains("source_type", "enrollment_id", "admission_id")
    def _check_billing_source(self):
        """Widen the billing source check's dependencies to Admission.

        The check itself (``_get_source_record()`` must be non-empty)
        is unchanged; only the trigger fields are widened so editing
        ``admission_id`` re-runs it. See ``_compute_partner_id`` for
        why the redeclaration is needed.

        :return: whatever ``super()._check_billing_source()`` returns
        """
        return super()._check_billing_source()

    @api.constrains("admission_id", "student_id")
    def _check_admission_student(self):
        """Require the Admission to already have a matching Student.

        ``school_admission.student_id`` is a plain ``res.partner`` --
        the contact used on the admission form, not the school-side
        Student record this waiver itself is keyed on
        (``school_fee_waiver.student_id``, comodel
        ``school_student``). The comparable field is
        ``school_admission.school_student_id``, only filled once the
        admission reaches state Open.

        :raises ValidationError: when ``admission_id`` is set and
            either its ``school_student_id`` is empty or differs from
            ``student_id``.
        """
        for record in self:
            if not record.admission_id:
                continue
            admission_student = record.admission_id.school_student_id
            if not admission_student:
                error_message = """
Document Type: %s
Context: Select waiver admission
Database ID: %s
Problem: Admission '%s' is not yet linked to student data
Solution: Select an Admission whose School Student has been set (Admission reaches Open)
""" % (
                    record._description,
                    record.id,
                    record.admission_id.display_name,
                )
                raise ValidationError(_(error_message))
            if admission_student != record.student_id:
                error_message = """
Document Type: %s
Context: Select waiver admission
Database ID: %s
Problem: Admission '%s' does not belong to Student '%s'
Solution: Select an Admission whose School Student matches the selected Student
""" % (
                    record._description,
                    record.id,
                    record.admission_id.display_name,
                    record.student_id.name,
                )
                raise ValidationError(_(error_message))

    def _get_source_record(self):
        """Return the Admission when Billing Source is Admission.

        :return: ``self.admission_id`` when ``source_type`` is
            ``admission``, otherwise whatever ``super()`` returns
        """
        self.ensure_one()
        if self.source_type == "admission":
            return self.admission_id
        return super()._get_source_record()

    def _get_source_payment_terms(self):
        """Return the Admission's payment terms for an Admission waiver.

        :return: ``school_admission_payment_term`` recordset when
            ``source_type`` is ``admission``, otherwise whatever
            ``super()`` returns
        """
        self.ensure_one()
        if self.source_type == "admission":
            return self.admission_id.payment_term_ids
        return super()._get_source_payment_terms()

    def _get_source_currency(self):
        """Return the Admission's currency for an Admission waiver.

        :return: ``res.currency`` record when ``source_type`` is
            ``admission``, otherwise whatever ``super()`` returns
        """
        self.ensure_one()
        if self.source_type == "admission":
            return self.admission_id.currency_id
        return super()._get_source_currency()

    def _prepare_schedule_term_data(self, payment_term):
        """Carry the Admission payment term onto a new Schedule line.

        :param payment_term: the payment term record being realized
        :return: dict setting ``admission_payment_term_id`` when
            ``source_type`` is ``admission``, otherwise whatever
            ``super()`` returns
        """
        self.ensure_one()
        if self.source_type == "admission":
            return {"admission_payment_term_id": payment_term.id}
        return super()._prepare_schedule_term_data(payment_term)
