# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolFeeWaiver(HttpSavepointCase):
    """Tour test for the Operating Unit auto-fill on ``school_fee_waiver``
    create.
    """

    @classmethod
    def setUpClass(cls):
        """Create the master data required by the create tour.

        Grants ``admin`` the multi operating unit group (Pre-Condition
        IK: Operating Unit is gated by
        ``groups="operating_unit.group_multi_operating_unit"``), and
        creates a School with exactly one Operating Unit so this
        module's derivation has something unambiguous to fill in.
        """
        super().setUpClass()
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.env.ref("operating_unit.group_multi_operating_unit").sudo().write(
            {"users": [(4, cls.user_admin.id)]}
        )

        ou_partner = cls.env["res.partner"].create(
            {"name": "TOUR OU FW Operating Unit Partner"}
        )
        cls.tour_operating_unit = cls.env["operating.unit"].create(
            {
                "name": "TOUR OU FW Operating Unit",
                "code": "TOUROUFW",
                "company_id": cls.env.ref("base.main_company").id,
                "partner_id": ou_partner.id,
            }
        )

        tour_grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR OU FW Grade Type",
                "code": "TOUROUFWGT",
            }
        )
        cls.tour_school = cls.env["school"].create(
            {
                "name": "TOUR OU FW School",
                "code": "TOUROUFWS",
                "grade_type_id": tour_grade_type.id,
                "operating_unit_ids": [(6, 0, [cls.tour_operating_unit.id])],
            }
        )
        tour_academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR OU FW Academic Year",
                "code": "TOUROUFWY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        tour_academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR OU FW Academic Term",
                "code": "TOUROUFWTM",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": tour_academic_year.id,
            }
        )
        tour_grade = cls.env["school_grade"].create(
            {
                "name": "TOUR OU FW Grade",
                "code": "TOUROUFWG",
                "type_id": tour_grade_type.id,
            }
        )
        tour_grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR OU FW Grade Class",
                "code": "TOUROUFWGC",
                "school_id": cls.tour_school.id,
                "grade_id": tour_grade.id,
            }
        )
        tour_contact = cls.env["res.partner"].create(
            {"name": "TOUR OU FW Student Contact"}
        )
        cls.tour_student = cls.env["school_student"].create(
            {
                "name": "TOUR OU FW Student",
                "code": "TOUROUFWST",
                "contact_id": tour_contact.id,
                "school_id": cls.tour_school.id,
            }
        )
        cls.tour_enrollment = cls.env["school_enrollment"].create(
            {
                # Manually assigned so the tour can pick this record
                # from the Enrollment m2o dropdown by typing
                # predictable text.
                "name": "TOUR-OU-FW-ENR-001",
                "academic_year_id": tour_academic_year.id,
                "academic_term_id": tour_academic_term.id,
                "school_id": cls.tour_school.id,
                "grade_id": tour_grade.id,
                "grade_class_id": tour_grade_class.id,
                "student_id": cls.tour_student.id,
            }
        )
        cls.tour_type = cls.env["school_fee_waiver_type"].create(
            {
                "name": "TOUR FW Type",
                "code": "TOUROUFWT",
            }
        )
        cls.tour_reason = cls.env["school_fee_waiver_reason"].create(
            {
                "name": "TOUR FW Reason",
                "code": "TOUROUFWR",
            }
        )

    def test_create(self):
        """Run the create tour for ``school_fee_waiver``.

        IK: docs/school_fee_waiver/01-create.md ("Additional
        Post-Condition" delta)
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_operating_unit_school_fee_waiver_create",
            login="admin",
        )
