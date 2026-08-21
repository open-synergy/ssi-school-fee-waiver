# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase
from psycopg2 import IntegrityError

from odoo.tests import tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiver(YamlTransactionCase):
    """Scenario-driven tests for the ``school_fee_waiver`` document."""

    def test_school_fee_waiver(self):
        """Run the ``school_fee_waiver`` create/workflow/constraint scenario.

        Covers create + computed field derivation, the full
        Draft -> Confirm -> Approve -> Open -> Done workflow, Cancel
        via the cancel-reason wizard, and every ``@api.constrains`` on
        ``school_fee_waiver`` and ``school_fee_waiver_line``, plus
        rejection of an approval attempt by a user with no approver
        group.
        """
        self.run_yaml_scenario("test_data_school_fee_waiver.yaml")

    def _create_required_header_field_fixtures(self):
        """Build the enrollment/type/reason fixture chain in Python.

        Pure Python fixture (trigger P10, L-09..L-11: the chain has no
        single ``EVAL:`` expression that can build it) shared by the
        three ``test_create_without_*`` methods below. Mirrors the
        ``fw1_*`` fixture chain in ``test_data_school_fee_waiver.yaml``
        but under a distinct ``FW2`` code prefix.

        :return: a dict with keys ``type_id``, ``reason_id``,
            ``student_id``, ``enrollment_id`` and ``payment_term_id``.
        """
        grade_type = self.env["school_grade_type"].create(
            {"name": "FW2 Grade Type", "code": "FW2GT"}
        )
        school = self.env["school"].create(
            {
                "name": "FW2 School",
                "code": "FW2SC",
                "grade_type_id": grade_type.id,
            }
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "FW2 Academic Year",
                "code": "FW2AY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = self.env["school_academic_term"].create(
            {
                "name": "FW2 Term",
                "code": "FW2TM",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        grade = self.env["school_grade"].create(
            {"name": "FW2 Grade", "code": "FW2GR", "type_id": grade_type.id}
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "FW2 Class",
                "code": "FW2CL",
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        contact = self.env["res.partner"].create({"name": "FW2 Contact"})
        student = self.env["school_student"].create(
            {
                "name": "FW2 Student",
                "code": "FW2ST",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        enrollment = self.env["school_enrollment"].create(
            {
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "grade_class_id": grade_class.id,
                "student_id": student.id,
            }
        )
        income_account_type = self.env.ref("account.data_account_type_revenue")
        income_account = self.env["account.account"].create(
            {
                "name": "FW2 Income Account",
                "code": "FW2IA",
                "user_type_id": income_account_type.id,
                "reconcile": False,
            }
        )
        product = self.env["product.product"].create(
            {"name": "FW2 Product", "type": "service"}
        )
        uom_unit = self.env.ref("uom.product_uom_unit")
        payment_term = self.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": enrollment.id,
                "name": "FW2 Term 1",
                "date_due": "2026-08-15",
                "detail_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "name": "FW2 Term 1 Fee",
                            "account_id": income_account.id,
                            "uom_quantity": 1.0,
                            "uom_id": uom_unit.id,
                            "price_unit": 1000000.0,
                        },
                    )
                ],
            }
        )
        waiver_type = self.env["school_fee_waiver_type"].create(
            {"name": "FW2 Type", "code": "FW2TY"}
        )
        waiver_reason = self.env["school_fee_waiver_reason"].create(
            {"name": "FW2 Reason", "code": "FW2RS"}
        )
        return {
            "type_id": waiver_type.id,
            "reason_id": waiver_reason.id,
            "student_id": student.id,
            "enrollment_id": enrollment.id,
            "coverage": "single_term",
            "payment_term_id": payment_term.id,
        }

    @mute_logger("odoo.sql_db")
    def test_create_without_type_must_be_rejected(self):
        """Reject a header create with no ``type_id`` at DB level.

        Pure Python -- trigger P5 (L-22: ``type_id`` is
        ``required=True``, i.e. a DB NOT NULL constraint, and
        ``psycopg2.IntegrityError`` is outside the 12 error types
        ``expect_error`` recognizes). ``mute_logger("odoo.sql_db")``
        silences the PostgreSQL ERROR line this raises; without it
        ``oca_checklog_odoo`` fails the CI even though the test
        passes.
        """
        values = self._create_required_header_field_fixtures()
        del values["type_id"]
        with self.assertRaises(IntegrityError):
            self.env["school_fee_waiver"].create(values)

    @mute_logger("odoo.sql_db")
    def test_create_without_reason_must_be_rejected(self):
        """Reject a header create with no ``reason_id`` at DB level.

        Pure Python -- trigger P5 (L-22: ``reason_id`` is
        ``required=True``, i.e. a DB NOT NULL constraint, and
        ``psycopg2.IntegrityError`` is outside the 12 error types
        ``expect_error`` recognizes). ``mute_logger("odoo.sql_db")``
        silences the PostgreSQL ERROR line this raises; without it
        ``oca_checklog_odoo`` fails the CI even though the test
        passes.
        """
        values = self._create_required_header_field_fixtures()
        del values["reason_id"]
        with self.assertRaises(IntegrityError):
            self.env["school_fee_waiver"].create(values)

    @mute_logger("odoo.sql_db")
    def test_create_without_student_must_be_rejected(self):
        """Reject a header create with no ``student_id`` at DB level.

        Pure Python -- trigger P5 (L-22: ``student_id`` is
        ``required=True``, i.e. a DB NOT NULL constraint, and
        ``psycopg2.IntegrityError`` is outside the 12 error types
        ``expect_error`` recognizes). ``mute_logger("odoo.sql_db")``
        silences the PostgreSQL ERROR line this raises; without it
        ``oca_checklog_odoo`` fails the CI even though the test
        passes.
        """
        values = self._create_required_header_field_fixtures()
        del values["student_id"]
        with self.assertRaises(IntegrityError):
            self.env["school_fee_waiver"].create(values)
