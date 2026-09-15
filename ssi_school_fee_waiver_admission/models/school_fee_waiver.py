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
    admission_payment_term_id = fields.Many2one(
        string="Admission Payment Term",
        comodel_name="school_admission_payment_term",
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Payment term this waiver closes out, restricted to "
        "payment terms of the selected Admission. Required when "
        "Billing Source is Admission and Coverage is Single Payment "
        "Term -- enforced by ``_check_coverage_payment_term``, not "
        "by this field itself. Must be empty when Coverage is "
        "Multiple Payment Terms.",
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

    @api.constrains("coverage", "payment_term_id", "admission_payment_term_id")
    def _check_coverage_payment_term(self):
        """Enforce Payment Term requiredness for the Admission subset.

        Widens the base check to also require/forbid
        ``admission_payment_term_id`` against ``coverage`` for
        waivers billed against an Admission. The non-Admission subset
        is left to ``super()`` unchanged -- it has no
        ``admission_payment_term_id`` to check. See
        ``_compute_partner_id`` for why the reduced-recordset
        ``super()`` call is needed.

        :raises ValidationError: when Coverage Single Payment Term
            has no ``admission_payment_term_id``, or Coverage
            Multiple Payment Terms has one set, on an Admission
            waiver.
        """
        admission_records = self.filtered(
            lambda record: record.source_type == "admission"
        )
        super(SchoolFeeWaiver, self - admission_records)._check_coverage_payment_term()
        for record in admission_records:
            if (
                record.coverage == "single_term"
                and not record.admission_payment_term_id
            ):
                error_message = """
Document Type: %s
Context: Set waiver coverage
Database ID: %s
Problem: Coverage 'Single Payment Term' requires an Admission Payment Term
Solution: Select the Admission Payment Term this waiver closes out
""" % (
                    record._description,
                    record.id,
                )
                raise ValidationError(_(error_message))
            if record.coverage == "multi_term" and record.admission_payment_term_id:
                error_message = """
Document Type: %s
Context: Set waiver coverage
Database ID: %s
Problem: Coverage 'Multiple Payment Terms' must not have an Admission Payment Term
Solution: Clear the Admission Payment Term, or switch Coverage to Single Payment Term
""" % (
                    record._description,
                    record.id,
                )
                raise ValidationError(_(error_message))

    @api.constrains("admission_payment_term_id", "admission_id", "source_type")
    def _check_admission_payment_term_admission(self):
        """Require the Admission Payment Term to belong to the Admission.

        Mirrors the base module's ``_check_payment_term_enrollment``,
        for the Admission Payment Term / Admission pairing instead of
        Payment Term / Enrollment.

        :raises ValidationError: when ``admission_payment_term_id``
            is set and its own ``admission_id`` differs from this
            waiver's ``admission_id``.
        """
        for record in self:
            if (
                record.source_type == "admission"
                and record.admission_payment_term_id
                and record.admission_id
                and record.admission_payment_term_id.admission_id != record.admission_id
            ):
                error_message = """
Document Type: %s
Context: Select waiver admission payment term
Database ID: %s
Problem: Admission Payment Term '%s' does not belong to Admission '%s'
Solution: Select an Admission Payment Term that belongs to the selected Admission
""" % (
                    record._description,
                    record.id,
                    record.admission_payment_term_id.display_name,
                    record.admission_id.display_name,
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

    def _get_schedule_payment_terms(self):
        """Return the Admission Payment Term for Single Term coverage.

        Only the Admission + Single Payment Term pairing needs its
        own body: Admission + Multiple Payment Terms is already
        covered by the base implementation, since it goes through
        ``_get_source_payment_terms()``, which this module overrides
        to resolve the Admission's own payment terms.

        :return: ``self.admission_payment_term_id`` filtered to
            non-cancelled state, when ``source_type`` is
            ``admission`` and ``coverage`` is ``single_term``;
            otherwise whatever ``super()`` returns
        """
        self.ensure_one()
        if self.source_type == "admission" and self.coverage == "single_term":
            return self.admission_payment_term_id.filtered(
                lambda term: term.state != "cancelled"
            )
        return super()._get_schedule_payment_terms()

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
