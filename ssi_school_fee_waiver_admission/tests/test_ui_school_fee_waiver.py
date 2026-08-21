# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolFeeWaiverAdmission(HttpSavepointCase):
    """Tour tests for the Admission Billing Source on ``school_fee_waiver``."""

    @classmethod
    def setUpClass(cls):
        """Create the master data required by the delta tours.

        Every record a tour types into an m2o must already exist,
        since a miss silently turns the pick step into a
        record-creation dialog. The Admission's contact is named
        exactly the text the tour types into Student -- the admission
        opening flow copies that name onto the School Student it
        auto-creates (``school_admission._10_create_school_student``),
        so typing it finds that same record rather than an unrelated
        one, which ``_check_admission_student`` would then reject.
        """
        super().setUpClass()
        cls.user_admin = cls.env.ref("base.user_admin")

        tour_grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR ADM FW Grade Type",
                "code": "TOURADMFWGT",
            }
        )
        cls.tour_school = cls.env["school"].create(
            {
                "name": "TOUR ADM FW School",
                "code": "TOURADMFWS",
                "grade_type_id": tour_grade_type.id,
            }
        )
        tour_academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR ADM FW Academic Year",
                "code": "TOURADMFWY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        tour_academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR ADM FW Academic Term",
                "code": "TOURADMFWTM",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": tour_academic_year.id,
            }
        )
        tour_grade = cls.env["school_grade"].create(
            {
                "name": "TOUR ADM FW Grade",
                "code": "TOURADMFWG",
                "type_id": tour_grade_type.id,
            }
        )

        cls.tour_type = cls.env["school_fee_waiver_type"].create(
            {
                "name": "TOUR ADM FW Type",
                "code": "TOURADMFWTY",
            }
        )
        cls.tour_reason = cls.env["school_fee_waiver_reason"].create(
            {
                "name": "TOUR ADM FW Reason",
                "code": "TOURADMFWRS",
            }
        )
        cls.tour_product = cls.env["product.product"].create(
            {
                "name": "TOUR ADM FW Product",
                "type": "service",
            }
        )

        # ── Pre-Condition for 01-create -- an Admission already Open,
        # named predictably so the tour can pick it from the m2o
        # dropdown.
        cls.tour_admission_contact = cls.env["res.partner"].create(
            {"name": "TOUR ADM FW Student"}
        )
        cls.tour_admission = cls.env["school_admission"].create(
            {
                "name": "TOUR-ADM-FW-ADM-001",
                "academic_year_id": tour_academic_year.id,
                "academic_term_id": tour_academic_term.id,
                "school_id": cls.tour_school.id,
                "grade_id": tour_grade.id,
                "student_id": cls.tour_admission_contact.id,
                # setUpClass runs as SUPERUSER, so without this the
                # record would be owned by superuser and record rule
                # school_admission_internal_user_rule
                # ([('user_id','=',user.id)]) would hide it from the
                # tour's own session, which logs in as admin.
                "user_id": cls.user_admin.id,
            }
        )
        # Advancing the fixture past its policy gate is Pre-Condition
        # setup, not the behaviour under test. Calling the transitions
        # bare would fail on approve_ok, which one shared compute
        # caches as False while action_confirm reads confirm_ok with
        # state still Draft (odoo-development-unit-test,
        # test-traps.md T-04).
        bypass = cls.tour_admission.with_context(bypass_policy_check=True)
        bypass.action_confirm()
        bypass.action_approve_approval()

        # ── Pre-Condition for 07-generate-schedule -- a second
        # Admission, an Admission-sourced waiver already On Progress
        # (one Schedule line auto-generated for the Payment Term that
        # existed at Open time), plus a second Payment Term added only
        # AFTER opening -- not covered by any Schedule line yet, so
        # the tour's click on Generate Schedule is what creates one
        # for it. Coverage's date range is deliberately wide (the
        # whole academic term) so it already covers the later-added
        # Term B without needing to change Coverage after the fact.
        gs_admission_contact = cls.env["res.partner"].create(
            {"name": "TOUR ADM FW GS Student"}
        )
        gs_admission = cls.env["school_admission"].create(
            {
                "academic_year_id": tour_academic_year.id,
                "academic_term_id": tour_academic_term.id,
                "school_id": cls.tour_school.id,
                "grade_id": tour_grade.id,
                "student_id": gs_admission_contact.id,
                "user_id": cls.user_admin.id,
            }
        )
        gs_bypass = gs_admission.with_context(bypass_policy_check=True)
        gs_bypass.action_confirm()
        gs_bypass.action_approve_approval()

        account_type_income = cls.env.ref("account.data_account_type_revenue")
        gs_income_account = cls.env["account.account"].create(
            {
                "name": "TOUR ADM FW GS Income Account",
                "code": "TOURADMFWGSIA",
                "user_type_id": account_type_income.id,
                "reconcile": False,
            }
        )
        # Term A is not referenced afterward -- it only needs to exist
        # so the waiver's first Generate Schedule (in setUpClass, via
        # the confirm/approve below) has something to schedule.
        cls.env["school_admission_payment_term"].create(
            {
                "admission_id": gs_admission.id,
                "name": "TOUR ADM FW SCHEDULE TERM A",
                "date_due": "2026-08-15",
                "detail_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.tour_product.id,
                            "name": "TOUR ADM FW GS Term A Fee",
                            "account_id": gs_income_account.id,
                            "uom_quantity": 1.0,
                            "uom_id": cls.env.ref("uom.product_uom_unit").id,
                            "price_unit": 1000000.0,
                        },
                    )
                ],
            }
        )
        cls.tour_waiver_generate_schedule = cls.env["school_fee_waiver"].create(
            {
                "name": "TOUR-ADM-FW-SCHEDULE-001",
                "type_id": cls.tour_type.id,
                "reason_id": cls.tour_reason.id,
                "student_id": gs_admission.school_student_id.id,
                "source_type": "admission",
                "admission_id": gs_admission.id,
                "coverage": "multi_term",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "user_id": cls.user_admin.id,
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
        )
        cls.tour_waiver_generate_schedule.action_confirm()
        # Same T-04 refresh reasoning as the Admission bypass above,
        # but through with_user(admin) since Approve must run as the
        # approval template's configured approver, not superuser.
        cls.tour_waiver_generate_schedule.invalidate_cache()
        cls.tour_waiver_generate_schedule.with_user(
            cls.user_admin
        ).action_approve_approval()
        # Added only now, after the waiver already opened (and thus
        # already auto-generated its Schedule against Term A alone) --
        # this is the Payment Term the tour's Generate Schedule click
        # is expected to pick up.
        cls.env["school_admission_payment_term"].create(
            {
                "admission_id": gs_admission.id,
                "name": "TOUR ADM FW SCHEDULE TERM B",
                "date_due": "2026-09-15",
                "detail_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.tour_product.id,
                            "name": "TOUR ADM FW GS Term B Fee",
                            "account_id": gs_income_account.id,
                            "uom_quantity": 1.0,
                            "uom_id": cls.env.ref("uom.product_uom_unit").id,
                            "price_unit": 500000.0,
                        },
                    )
                ],
            }
        )

    def test_create(self):
        """Run the create tour's Admission billing source delta.

        IK: docs/school_fee_waiver/01-create.md ("Additional Fields"
        delta)
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_admission_school_fee_waiver_create",
            login="admin",
        )

    def test_generate_schedule(self):
        """Run the generate schedule tour's Admission billing source
        delta.

        IK: docs/school_fee_waiver/07-generate-schedule.md
        ("Additional Behavior" delta)
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_admission_school_fee_waiver_generate_schedule",
            login="admin",
        )
