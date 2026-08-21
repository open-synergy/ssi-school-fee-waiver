# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolFeeWaiver(HttpSavepointCase):
    """Tour tests for the ``school_fee_waiver`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the master data and waivers required by the tours."""
        super().setUpClass()
        admin = cls.env.ref("base.user_admin")

        # Pre-Condition -- School/Academic Year/Grade/Grade Class/
        # Student, so an Enrollment can be created for the tour
        # Student.
        tour_grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR FW Grade Type",
                "code": "TOURFWGT",
            }
        )
        tour_school = cls.env["school"].create(
            {
                "name": "TOUR FW School",
                "code": "TOURFWSC",
                "grade_type_id": tour_grade_type.id,
            }
        )
        tour_academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR FW Academic Year",
                "code": "TOURFWAY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        tour_academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR FW Academic Term",
                "code": "TOURFWTM",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": tour_academic_year.id,
            }
        )
        tour_grade = cls.env["school_grade"].create(
            {
                "name": "TOUR FW Grade",
                "code": "TOURFWGR",
                "type_id": tour_grade_type.id,
            }
        )
        tour_grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR FW Grade Class",
                "code": "TOURFWGC",
                "school_id": tour_school.id,
                "grade_id": tour_grade.id,
            }
        )
        tour_contact = cls.env["res.partner"].create(
            {
                "name": "TOUR FW Student Contact",
            }
        )
        cls.tour_student = cls.env["school_student"].create(
            {
                "name": "TOUR FW Student",
                "code": "TOURFWST",
                "contact_id": tour_contact.id,
                "school_id": tour_school.id,
            }
        )
        cls.tour_enrollment = cls.env["school_enrollment"].create(
            {
                # Manually assigned so the tour can pick this record
                # from the Enrollment m2o dropdown by typing
                # predictable text.
                "name": "TOUR-FW-ENR-001",
                "academic_year_id": tour_academic_year.id,
                "academic_term_id": tour_academic_term.id,
                "school_id": tour_school.id,
                "grade_id": tour_grade.id,
                "grade_class_id": tour_grade_class.id,
                "student_id": cls.tour_student.id,
            }
        )

        # Pre-Condition -- Type, Reason, Product, Income Account, and
        # one shared Payment Term. The Payment Term is safely reused
        # across every Single Payment Term fixture below: the
        # (Line, Payment Term) uniqueness constraint is scoped per
        # Line, and every fixture waiver creates its own Line.
        account_type_income = cls.env.ref("account.data_account_type_revenue")
        tour_income_account = cls.env["account.account"].create(
            {
                "name": "TOUR FW Income Account",
                "code": "TOURFWIA",
                "user_type_id": account_type_income.id,
                "reconcile": False,
            }
        )
        cls.tour_product = cls.env["product.product"].create(
            {
                "name": "TOUR FW Product",
                "type": "service",
            }
        )
        cls.tour_type = cls.env["school_fee_waiver_type"].create(
            {
                "name": "TOUR FW Type",
                "code": "TOURFWTY",
            }
        )
        cls.tour_reason = cls.env["school_fee_waiver_reason"].create(
            {
                "name": "TOUR FW Reason",
                "code": "TOURFWRS",
            }
        )
        cls.tour_term = cls.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": cls.tour_enrollment.id,
                "name": "TOUR-FW-TERM-001",
                "date_due": "2026-08-15",
                "detail_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.tour_product.id,
                            "name": "TOUR FW Term Fee",
                            "account_id": tour_income_account.id,
                            "uom_quantity": 1.0,
                            "uom_id": cls.env.ref("uom.product_uom_unit").id,
                            "price_unit": 1000000.0,
                        },
                    )
                ],
            }
        )

        def make_waiver(name, **extra_values):
            """Create a Single Payment Term waiver fixture.

            :param name: value assigned to the waiver's ``name`` so a
                tour can find this exact row in the list by its text
            :param extra_values: additional ``school_fee_waiver``
                values, merged over the common defaults
            :return: the created ``school_fee_waiver`` record
            """
            values = {
                "name": name,
                "type_id": cls.tour_type.id,
                "reason_id": cls.tour_reason.id,
                "student_id": cls.tour_student.id,
                "enrollment_id": cls.tour_enrollment.id,
                "coverage": "single_term",
                "payment_term_id": cls.tour_term.id,
                "user_id": admin.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.tour_product.id,
                            "computation": "full",
                        },
                    )
                ],
            }
            values.update(extra_values)
            return cls.env["school_fee_waiver"].create(values)

        # Pre-Condition for 04-confirm -- a Draft waiver with one Line.
        cls.tour_waiver_confirm = make_waiver("TOUR-FW-CONFIRM-001")

        # Pre-Condition for 05-approve -- already pushed to Waiting for
        # Approval in Python via ``action_confirm()``, since Confirm
        # itself is exercised by 04-confirm.md's own tour.
        cls.tour_waiver_approve = make_waiver("TOUR-FW-APPROVE-001")
        cls.tour_waiver_approve.action_confirm()

        # Pre-Condition for 06-reject -- same shape as 05-approve.
        cls.tour_waiver_reject = make_waiver("TOUR-FW-REJECT-001")
        cls.tour_waiver_reject.action_confirm()

        # Pre-Condition for 07-generate-schedule -- a Multiple Payment
        # Terms waiver already On Progress (one Schedule line
        # auto-generated for the Payment Term that existed at Open
        # time), plus a second Payment Term added only AFTER opening
        # -- not covered by any Schedule line yet, so the tour's click
        # on Generate Schedule is what creates one for it.
        cls.tour_waiver_generate_schedule = make_waiver(
            "TOUR-FW-SCHEDULE-001",
            coverage="multi_term",
            payment_term_id=False,
            date_start="2026-07-01",
            date_end="2026-12-31",
        )
        cls.tour_waiver_generate_schedule.action_confirm()
        # ``approve_ok`` shares its compute method (``_compute_policy``)
        # with every other policy field, and that method only
        # re-triggers on ``@api.depends("policy_template_id")`` -- the
        # confirm step above already cached approve_ok=False (no
        # approver existed yet), so it must be busted explicitly
        # before Approve reads it (odoo-development-unit-test,
        # test-traps.md T-04). Approve also runs ``with_user(admin)``,
        # not as ``cls.env``'s superuser: the approve policy's
        # ``restrict_additional`` check tests ``env.user.id in
        # document.active_approver_user_ids.ids`` unconditionally, and
        # only ``admin`` -- the approval template's configured
        # approver -- is ever in that list.
        cls.tour_waiver_generate_schedule.invalidate_cache()
        cls.tour_waiver_generate_schedule.with_user(admin).action_approve_approval()
        cls.tour_term_new = cls.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": cls.tour_enrollment.id,
                "name": "TOUR FW SCHEDULE TERM B",
                "date_due": "2026-09-15",
                "detail_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.tour_product.id,
                            "name": "TOUR FW Term B Fee",
                            "account_id": tour_income_account.id,
                            "uom_quantity": 1.0,
                            "uom_id": cls.env.ref("uom.product_uom_unit").id,
                            "price_unit": 500000.0,
                        },
                    )
                ],
            }
        )

        # Pre-Condition for 09-finish -- On Progress, same recipe as
        # 07-generate-schedule's approve step above.
        cls.tour_waiver_finish = make_waiver("TOUR-FW-FINISH-001")
        cls.tour_waiver_finish.action_confirm()
        cls.tour_waiver_finish.invalidate_cache()
        cls.tour_waiver_finish.with_user(admin).action_approve_approval()

        # Pre-Condition for 10-cancel -- a Draft waiver, plus the
        # Cancellation Reason the wizard requires.
        cls.tour_waiver_cancel = make_waiver("TOUR-FW-CANCEL-001")
        cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR FW Cancel Reason",
                "code": "TOURFWCR",
                # The cancel wizard's radio widget only lists reasons
                # in ir.model.all_cancel_reason_ids, which merges
                # model-specific links with every global_use=True
                # reason. Without this, the tour's radio option never
                # renders.
                "global_use": True,
            }
        )

        # Pre-Condition for 12-restart -- already Cancelled. Written
        # directly rather than through the wizard, since the cancel
        # mechanism itself is exercised by 10-cancel.md's own tour.
        cls.tour_waiver_restart = make_waiver("TOUR-FW-RESTART-001")
        cls.tour_waiver_restart.write({"state": "cancel"})

        # Pre-Condition for 14-restart-approval -- Waiting for
        # Approval, same recipe as 06-reject.
        cls.tour_waiver_restart_approval = make_waiver("TOUR-FW-RESTARTAPPR-001")
        cls.tour_waiver_restart_approval.action_confirm()

    def test_create(self):
        """Run the create tour for ``school_fee_waiver``.

        IK: docs/school_fee_waiver/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_school_fee_waiver_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``school_fee_waiver``.

        IK: docs/school_fee_waiver/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_school_fee_waiver_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``school_fee_waiver``.

        IK: docs/school_fee_waiver/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_school_fee_waiver_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``school_fee_waiver``.

        IK: docs/school_fee_waiver/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_school_fee_waiver_reject",
            login="admin",
        )

    def test_generate_schedule(self):
        """Run the generate schedule tour for ``school_fee_waiver``.

        IK: docs/school_fee_waiver/07-generate-schedule.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_school_fee_waiver_generate_schedule",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour for ``school_fee_waiver``.

        IK: docs/school_fee_waiver/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_school_fee_waiver_finish",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_fee_waiver``.

        IK: docs/school_fee_waiver/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_school_fee_waiver_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``school_fee_waiver``.

        IK: docs/school_fee_waiver/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_school_fee_waiver_restart",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval tour for ``school_fee_waiver``.

        IK: docs/school_fee_waiver/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_school_fee_waiver_restart_approval",
            login="admin",
        )
