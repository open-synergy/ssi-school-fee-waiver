# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolFeeWaiver(models.Model):
    """
    Represents a request to reduce part of a student's billed fees.
    A fee waiver differs from a promotion discount
    (``ssi_school_promotion``) in the shape of the request itself: one
    waiver may close out a single payment term (``coverage`` =
    ``single_term``), or repeat over every payment term of its billing
    source that falls within a date range (``coverage`` =
    ``multi_term``). Each waiver Line names a billing component
    (Product or Product Category) and how much of it is waived; once
    the waiver is Open, ``action_generate_schedule`` -- triggered
    automatically -- expands every Line into one Schedule line per
    matching payment term, with the waived amount already computed
    against that term's actual billed amount. This document never
    posts a journal entry nor fills in the realized amount itself --
    that is ``ssi_school_fee_waiver_deduction``, a later module out of
    this item's scope. The billing source is deliberately extensible:
    this module only registers Enrollment, following the same
    ``_get_source_*`` hook pattern as ``school_scholarship_award``, so
    a later glue module can register Admission without touching this
    model's structure. The waiver follows the standard SSI five-state
    workflow: Draft -> Confirm -> Approve -> Open -> Done, and can
    also reach Cancel.
    """

    _name = "school_fee_waiver"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.company_currency",
        "mixin.localdict",
    ]
    _description = "School Fee Waiver"
    _order = "date desc, id desc"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_open_button = False

    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
        "generate_schedule_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_generate_schedule",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_done",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    date = fields.Date(
        string="Date",
        default=lambda r: datetime_date.today(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The date of this fee waiver document.",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="school_fee_waiver_type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="School-defined classification of this fee waiver.",
    )
    reason_id = fields.Many2one(
        string="Reason",
        comodel_name="school_fee_waiver_reason",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Reason the applicant is requesting this fee waiver.",
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="school_student",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Student this fee waiver is granted to.",
    )
    source_type = fields.Selection(
        string="Billing Source",
        selection=[
            ("enrollment", "Enrollment"),
        ],
        default="enrollment",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Billing source this waiver is billed against. This "
        "module only registers Enrollment -- extension modules add "
        "further values with ``selection_add`` and override the "
        "``_get_source_*`` hooks to match.",
    )
    enrollment_id = fields.Many2one(
        string="Enrollment",
        comodel_name="school_enrollment",
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Enrollment this waiver is billed against. Must belong "
        "to the selected Student. Required when Billing Source is "
        "Enrollment -- enforced by ``_check_billing_source``, not by "
        "this field itself, so an extension module's own billing "
        "source is not forced to also be a required field.",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        compute="_compute_partner_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Contact partner of this waiver's billing source.",
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        compute="_compute_school_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="School of the selected billing source.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        compute="_compute_grade_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Grade of the selected billing source.",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        compute="_compute_academic_year_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Academic year of the selected billing source.",
    )
    coverage = fields.Selection(
        string="Coverage",
        selection=[
            ("single_term", "Single Payment Term"),
            ("multi_term", "Multiple Payment Terms"),
        ],
        default="single_term",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Single Payment Term closes out exactly one payment "
        "term, selected below. Multiple Payment Terms repeats this "
        "waiver over every payment term of the billing source that "
        "falls within Start Date/End Date.",
    )
    payment_term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="school_enrollment_payment_term",
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Payment term this waiver closes out. Required when "
        "Coverage is Single Payment Term; must be empty when Coverage "
        "is Multiple Payment Terms.",
    )
    date_start = fields.Date(
        string="Start Date",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="First date a payment term must fall on or after to be "
        "covered, when Coverage is Multiple Payment Terms. Empty "
        "means no lower bound.",
    )
    date_end = fields.Date(
        string="End Date",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Last date a payment term must fall on or before to be "
        "covered, when Coverage is Multiple Payment Terms. Empty "
        "means no upper bound.",
    )
    note = fields.Text(
        string="Note",
        help="Free-form note about this fee waiver.",
    )
    line_ids = fields.One2many(
        string="Lines",
        comodel_name="school_fee_waiver_line",
        inverse_name="waiver_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Billing components covered by this waiver, and how much "
        "of each is waived. At least one line is expected before "
        "this waiver is confirmed.",
    )
    schedule_ids = fields.One2many(
        string="Schedule",
        comodel_name="school_fee_waiver_schedule",
        inverse_name="waiver_id",
        help="Realization schedule of this waiver, one line per "
        "Line/payment term pairing, generated by Generate Schedule.",
    )
    amount_waived = fields.Monetary(
        string="Amount Waived",
        currency_field="company_currency_id",
        compute="_compute_amount_waived",
        store=True,
        compute_sudo=True,
        help="Total value of this waiver, computed as the sum of its "
        "Schedule lines' Amount Planned, excluding Skipped and "
        "Cancelled lines. Empty until a Schedule exists -- see "
        "Generate Schedule.",
    )
    generate_schedule_ok = fields.Boolean(
        string="Can Generate Schedule",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help="Policy that determines whether the per-term waiver "
        "schedule may be generated for this document.",
    )

    @api.depends("enrollment_id")
    def _compute_partner_id(self):
        """Derive the Partner from this waiver's billing source.

        Extension point: a module registering another Billing Source
        value declares a new method decorated with its own
        ``@api.depends`` (e.g. ``"admission_id"``) that calls
        ``super()`` first, so this method's own ``enrollment_id``
        dependency keeps working unmodified.

        :return: nothing; assigns ``partner_id``
        """
        for record in self:
            source = record._get_source_record()
            record.partner_id = source.partner_id if source else False

    @api.depends("enrollment_id")
    def _compute_school_id(self):
        """Derive the School from this waiver's billing source.

        See ``_compute_partner_id`` for the extension pattern this
        method follows.

        :return: nothing; assigns ``school_id``
        """
        for record in self:
            source = record._get_source_record()
            record.school_id = source.school_id if source else False

    @api.depends("enrollment_id")
    def _compute_grade_id(self):
        """Derive the Grade from this waiver's billing source.

        See ``_compute_partner_id`` for the extension pattern this
        method follows.

        :return: nothing; assigns ``grade_id``
        """
        for record in self:
            source = record._get_source_record()
            record.grade_id = source.grade_id if source else False

    @api.depends("enrollment_id")
    def _compute_academic_year_id(self):
        """Derive the Academic Year from this waiver's billing source.

        See ``_compute_partner_id`` for the extension pattern this
        method follows.

        :return: nothing; assigns ``academic_year_id``
        """
        for record in self:
            source = record._get_source_record()
            record.academic_year_id = source.academic_year_id if source else False

    @api.depends("schedule_ids.amount_planned", "schedule_ids.state")
    def _compute_amount_waived(self):
        """Sum the Schedule lines into the waiver's waived amount.

        Skipped and Cancelled lines are excluded: they represent a
        term that was scheduled and then withdrawn, not a live
        waiver.

        :return: nothing; assigns ``amount_waived``
        """
        for record in self:
            lines = record.schedule_ids.filtered(
                lambda schedule: schedule.state not in ("skipped", "cancelled")
            )
            record.amount_waived = sum(lines.mapped("amount_planned"))

    @api.constrains("source_type", "enrollment_id")
    def _check_billing_source(self):
        """Require a billing source record for the selected source type.

        The requiredness of ``enrollment_id`` lives here rather than
        on the field itself so an extension module's Billing Source
        value is not forced to also key off ``enrollment_id``: each
        value's own source field is validated through
        ``_get_source_record()`` instead.

        :raises ValidationError: when ``_get_source_record()`` is
            empty.
        """
        for record in self:
            if not record._get_source_record():
                error_message = """
Document Type: %s
Context: Set waiver billing source
Database ID: %s
Problem: No billing source record set for Billing Source '%s'
Solution: Select the record matching the selected Billing Source
""" % (
                    record._description,
                    record.id,
                    record.source_type,
                )
                raise ValidationError(_(error_message))

    @api.constrains("coverage", "payment_term_id")
    def _check_coverage_payment_term(self):
        """Enforce Payment Term requiredness against Coverage.

        Single Payment Term requires ``payment_term_id``; Multiple
        Payment Terms forbids it -- the schedule is derived from the
        date range instead.

        :raises ValidationError: when the pairing of ``coverage`` and
            ``payment_term_id`` does not match either rule above.
        """
        for record in self:
            if record.coverage == "single_term" and not record.payment_term_id:
                error_message = """
Document Type: %s
Context: Set waiver coverage
Database ID: %s
Problem: Coverage 'Single Payment Term' requires a Payment Term
Solution: Select the Payment Term this waiver closes out
""" % (
                    record._description,
                    record.id,
                )
                raise ValidationError(_(error_message))
            if record.coverage == "multi_term" and record.payment_term_id:
                error_message = """
Document Type: %s
Context: Set waiver coverage
Database ID: %s
Problem: Coverage 'Multiple Payment Terms' must not have a Payment Term
Solution: Clear the Payment Term, or switch Coverage to Single Payment Term
""" % (
                    record._description,
                    record.id,
                )
                raise ValidationError(_(error_message))

    @api.constrains("payment_term_id", "enrollment_id", "source_type")
    def _check_payment_term_enrollment(self):
        """Require the selected Payment Term to belong to the source.

        Guarded to Billing Source Enrollment: an extension module's
        billing source is not billed against an Enrollment at all, so
        this check has nothing to compare for it.

        :raises ValidationError: when ``payment_term_id`` is set and
            does not belong to ``enrollment_id``.
        """
        for record in self:
            if (
                record.source_type == "enrollment"
                and record.payment_term_id
                and record.enrollment_id
                and record.payment_term_id.enrollment_id != record.enrollment_id
            ):
                error_message = """
Document Type: %s
Context: Select waiver payment term
Database ID: %s
Problem: Payment Term '%s' does not belong to Enrollment '%s'
Solution: Select a Payment Term that belongs to the selected Enrollment
""" % (
                    record._description,
                    record.id,
                    record.payment_term_id.display_name,
                    record.enrollment_id.display_name,
                )
                raise ValidationError(_(error_message))

    @ssi_decorator.pre_confirm_action()
    def _10_check_line(self):
        """Reject confirming a waiver with no Line.

        :raises UserError: when ``line_ids`` is empty.
        """
        self.ensure_one()
        if not self.line_ids:
            error_message = """
Document Type: %s
Context: Confirm waiver
Database ID: %s
Problem: Waiver has no Line
Solution: Add at least one Line before confirming
""" % (
                self._description,
                self.id,
            )
            raise UserError(_(error_message))

    @ssi_decorator.pre_cancel_action()
    def _10_check_realized_schedule(self):
        """Reject cancelling a waiver with a realized Schedule line.

        :raises UserError: when any of this waiver's Schedule lines is
            in state ``realized``.
        """
        self.ensure_one()
        realized = self.schedule_ids.filtered(
            lambda schedule: schedule.state == "realized"
        )
        if realized:
            error_message = """
Document Type: %s
Context: Cancel waiver
Database ID: %s
Problem: Waiver has a realized Schedule line
Solution: The realized period can no longer be withdrawn by cancelling this waiver
""" % (
                self._description,
                self.id,
            )
            raise UserError(_(error_message))

    @ssi_decorator.post_open_action()
    def _10_generate_schedule(self):
        """Auto-generate the Schedule once the waiver reaches Open.

        :return: nothing; delegates to ``_generate_schedule``
        """
        self.ensure_one()
        self._generate_schedule(bypass_policy_check=True)

    def action_generate_schedule(self):
        """Generate this waiver's per-term Schedule lines."""
        for record in self.sudo():
            record._generate_schedule()

    def _generate_schedule(self, bypass_policy_check=False):
        """Regenerate this waiver's Schedule lines.

        Every Schedule line still in ``draft`` or ``scheduled`` is
        deleted first, then one fresh line is (re)created per Line ×
        matching payment term pairing. A pairing that already has a
        Schedule line in ``realized``, ``skipped``, or ``cancelled``
        is left untouched -- it is never a match target for deletion
        or a duplicate target for creation, so a period already
        settled or withdrawn survives regeneration unchanged. The
        pairing is matched through each existing Schedule line's own
        ``_get_source_term()`` -- its effective source term -- rather
        than the raw ``payment_term_id`` field, so an extension module
        that keys its Schedule lines off a different source field
        (e.g. ``admission_payment_term_id``) is still matched
        correctly and does not get its already-realized/skipped/
        cancelled lines duplicated.

        :param bypass_policy_check: skip the ``generate_schedule_ok``
            policy check, used when called from
            ``_10_generate_schedule`` right after ``action_open``
        :return: nothing; creates/deletes
            ``school_fee_waiver_schedule`` records
        """
        self.ensure_one()
        if not bypass_policy_check:
            self._check_generate_schedule_policy()
        stale = self.schedule_ids.filtered(
            lambda schedule: schedule.state in ("draft", "scheduled")
        )
        stale.unlink()
        terms = self._get_schedule_payment_terms()
        for line in self.line_ids:
            scheduled_term_ids = line.schedule_ids.mapped(
                lambda schedule: schedule._get_source_term().id
            )
            for term in terms:
                if term.id in scheduled_term_ids:
                    continue
                self.env["school_fee_waiver_schedule"].create(
                    self._prepare_schedule_data(line, term)
                )

    def _check_generate_schedule_policy(self):
        """Reject schedule generation when the policy check fails.

        ``generate_schedule_ok`` is invalidated first: it is a
        ``mixin.policy`` field whose compute only depends on
        ``policy_template_id`` (not ``state``), so a value cached
        before this waiver reached Open would otherwise still read as
        stale when called right after ``action_open`` writes the new
        state.

        :raises UserError: when ``generate_schedule_ok`` is falsy.
        :return: ``True``
        """
        self.ensure_one()
        self.invalidate_cache(fnames=["generate_schedule_ok"], ids=self.ids)
        if not self.generate_schedule_ok:
            error_message = """
Document Type: %s
Context: Generate waiver schedule
Database ID: %s
Problem: Document is not allowed to generate schedule
Solution: Check generate schedule policy prerequisite
""" % (
                self._description,
                self.id,
            )
            raise UserError(_(error_message))
        return True

    def _get_schedule_payment_terms(self):
        """List the payment terms this waiver's Schedule is built over.

        Single Payment Term always yields exactly the selected
        ``payment_term_id``; Multiple Payment Terms yields every
        payment term of the billing source whose ``date_due`` falls
        within ``date_start``..``date_end`` (an empty bound is
        unlimited on that side). A payment term in state
        ``cancelled`` is always excluded, on either coverage.

        :return: ``school_enrollment_payment_term`` recordset
        """
        self.ensure_one()
        if self.coverage == "single_term":
            terms = self.payment_term_id
        else:
            terms = self._get_source_payment_terms()
            if self.date_start:
                terms = terms.filtered(
                    lambda term: term.date_due and term.date_due >= self.date_start
                )
            if self.date_end:
                terms = terms.filtered(
                    lambda term: term.date_due and term.date_due <= self.date_end
                )
        return terms.filtered(lambda term: term.state != "cancelled")

    def _prepare_schedule_data(self, line, term):
        """Build the ``school_fee_waiver_schedule`` values for a pairing.

        :param line: the ``school_fee_waiver_line`` record being
            scheduled
        :param term: the ``school_enrollment_payment_term`` this line
            realizes
        :return: dict of ``school_fee_waiver_schedule`` values
        """
        self.ensure_one()
        result = {
            "waiver_id": self.id,
            "line_id": line.id,
            "date": term.date_due,
            "state": "scheduled",
        }
        result.update(self._prepare_schedule_term_data(term))
        return result

    def _get_source_record(self):
        """Return the billing source record backing this waiver.

        Extension point: a module registering another Billing Source
        value overrides this together with ``source_type``'s
        ``selection_add`` to point at that value's own source record
        instead.

        :return: recordset of the billing source (``school_enrollment``
            in this module), possibly empty
        """
        self.ensure_one()
        return self.enrollment_id

    def _get_source_payment_terms(self):
        """Return the payment terms of this waiver's billing source.

        :return: ``school_enrollment_payment_term`` recordset,
            possibly empty
        """
        self.ensure_one()
        return self.enrollment_id.payment_term_ids

    def _get_source_currency(self):
        """Return the currency of this waiver's billing source.

        :return: ``res.currency`` record, or an empty recordset when
            no billing source is set
        """
        self.ensure_one()
        return self.enrollment_id.currency_id

    def _prepare_schedule_term_data(self, payment_term):
        """Build the payment-term-specific Schedule line values.

        Extension point: a module giving Schedule an extra source
        field of its own overrides this to fill that field instead of
        ``payment_term_id``.

        :param payment_term: the payment term this Schedule line
            realizes
        :return: dict of ``school_fee_waiver_schedule`` values
        """
        self.ensure_one()
        return {"payment_term_id": payment_term.id}

    @api.model
    def _get_policy_field(self):
        """Register this model's policy fields for ``mixin.policy``.

        ``open_ok`` (from ``mixin.transaction_open``) must be listed
        here too: Odoo requires every field sharing the same
        ``compute`` method (``_compute_policy``) to be assigned a
        value on every call, and ``mixin.transaction_open`` itself
        never registers it -- omitting it here raises
        ``ValueError: Compute method failed to assign ...open_ok``
        as soon as the field is read (e.g. rendering the form view).

        :return: the base policy fields plus this model's own
            ``generate_schedule_ok``
        """
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "restart_approval_ok",
            "done_ok",
            "cancel_ok",
            "restart_ok",
            "manual_number_ok",
            "open_ok",
            "generate_schedule_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        """Reconfigure the statusbar's visible states on the form view.

        :param view_arch: the parsed form view architecture
        :return: the (possibly modified) view architecture
        """
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
