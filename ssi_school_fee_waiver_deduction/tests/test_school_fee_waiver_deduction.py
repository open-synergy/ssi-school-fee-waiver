# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged
from odoo.tools.float_utils import float_compare


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverDeduction(YamlTransactionCase):
    """Scenario tests for ``school_fee_waiver_deduction``."""

    def test_school_fee_waiver_deduction(self):
        """Run the create/workflow/reconcile/cancel/constraints scenario."""
        self.run_yaml_scenario("test_data_school_fee_waiver_deduction.yaml")

    def test_partial_allocation_float_precision(self):
        """Assert a fractional partial-allocation residual with tolerance.

        P2 (L-04): ``odoo-yaml-test``'s ``equals`` operator is a raw
        ``!=`` with no ``delta``/``float_compare`` tolerance, so a
        fractional partial-allocation residual can only be asserted
        safely from Python.
        """
        admin = self.env.ref("base.user_admin")

        grade_type = self.env["school_grade_type"].create(
            {"name": "P2 Grade Type", "code": "P2GT"}
        )
        school = self.env["school"].create(
            {
                "name": "P2 School",
                "code": "P2SC",
                "grade_type_id": grade_type.id,
            }
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "P2 Academic Year",
                "code": "P2AY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = self.env["school_academic_term"].create(
            {
                "name": "P2 Term",
                "code": "P2TM",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        grade = self.env["school_grade"].create(
            {"name": "P2 Grade", "code": "P2GR", "type_id": grade_type.id}
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "P2 Class",
                "code": "P2CL",
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        contact = self.env["res.partner"].create({"name": "P2 Contact"})
        student = self.env["school_student"].create(
            {
                "name": "P2 Student",
                "code": "P2ST",
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

        receivable_type = self.env.ref("account.data_account_type_receivable")
        income_type = self.env.ref("account.data_account_type_revenue")
        expense_type = self.env.ref("account.data_account_type_expenses")
        receivable_account = self.env["account.account"].create(
            {
                "name": "P2 Receivable Account",
                "code": "P2RA",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        income_account = self.env["account.account"].create(
            {
                "name": "P2 Income Account",
                "code": "P2IA",
                "user_type_id": income_type.id,
            }
        )
        discount_account = self.env["account.account"].create(
            {
                "name": "P2 Discount Account",
                "code": "P2DA",
                "user_type_id": expense_type.id,
            }
        )
        deduction_journal = self.env["account.journal"].create(
            {"name": "P2 Deduction Journal", "code": "P2DJ", "type": "general"}
        )
        sale_journal = self.env["account.journal"].create(
            {"name": "P2 Sale Journal", "code": "P2SJ", "type": "sale"}
        )
        product = self.env["product.product"].create(
            {"name": "P2 Product", "type": "service"}
        )
        # Term billed at 100.00, so a 33.33 partial allocation leaves a
        # residual of 66.67 -- the fractional value this test exists to
        # assert with tolerance.
        term = self.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": enrollment.id,
                "name": "P2 Term",
                "date_due": "2026-08-15",
                "detail_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "name": "P2 Term Fee",
                            "account_id": income_account.id,
                            "uom_quantity": 1.0,
                            "uom_id": self.env.ref("uom.product_uom_unit").id,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )

        waiver_type = self.env["school_fee_waiver_type"].create(
            {
                "name": "P2 Type",
                "code": "P2TY",
                "deduction_journal_id": deduction_journal.id,
                "discount_account_id": discount_account.id,
            }
        )
        reason = self.env["school_fee_waiver_reason"].create(
            {"name": "P2 Reason", "code": "P2RS"}
        )
        waiver = self.env["school_fee_waiver"].create(
            {
                "type_id": waiver_type.id,
                "reason_id": reason.id,
                "student_id": student.id,
                "enrollment_id": enrollment.id,
                "coverage": "single_term",
                "payment_term_id": term.id,
                "user_id": admin.id,
                "line_ids": [(0, 0, {"product_id": product.id, "computation": "full"})],
            }
        )
        waiver = waiver.with_user(admin)
        waiver.action_confirm()
        waiver.invalidate_cache()
        waiver.action_approve_approval()
        schedule = waiver.schedule_ids
        self.assertEqual(len(schedule), 1)

        invoice_type = self.env["customer_invoice_type"].create(
            {
                "name": "P2 Invoice Type",
                "code": "/",
                "journal_id": sale_journal.id,
                "receivable_account_id": receivable_account.id,
            }
        )
        invoice = self.env["customer_invoice"].create(
            {
                "type_id": invoice_type.id,
                "partner_id": contact.id,
                "date": "2026-08-20",
                "date_due": "2026-09-20",
                "currency_id": self.env.company.currency_id.id,
                "journal_id": sale_journal.id,
                "receivable_account_id": receivable_account.id,
            }
        )
        self.env["customer_invoice.line"].create(
            {
                "customer_invoice_id": invoice.id,
                "name": "Line",
                "account_id": income_account.id,
                "uom_quantity": 1,
                "price_unit": 100.0,
            }
        )
        invoice = invoice.with_user(admin)
        invoice.action_confirm()
        invoice.invalidate_cache()
        invoice.action_approve_approval()

        deduction = self.env["school_fee_waiver_deduction"].create(
            {
                "waiver_id": waiver.id,
                "journal_id": deduction_journal.id,
                "receivable_account_id": receivable_account.id,
            }
        )
        self.env["school_fee_waiver_deduction_line"].create(
            {
                "deduction_id": deduction.id,
                "schedule_id": schedule.id,
                "account_id": discount_account.id,
                # Matches the allocation below exactly, so Amount
                # Unallocated is zero and the pre-open gate passes --
                # the fractional value under test is the invoice's own
                # residual after this PARTIAL allocation, not this
                # line's own amount.
                "amount": 33.33,
            }
        )
        self.env["school_fee_waiver_deduction_allocation"].create(
            {
                "deduction_id": deduction.id,
                "customer_invoice_id": invoice.id,
                "amount": 33.33,
            }
        )
        deduction = deduction.with_user(admin)
        deduction.action_confirm()
        deduction.invalidate_cache()
        deduction.action_approve_approval()

        precision = self.env.company.currency_id.decimal_places
        self.assertEqual(
            float_compare(
                deduction.amount_unallocated, 0.0, precision_digits=precision
            ),
            0,
        )
        self.assertEqual(
            float_compare(invoice.amount_residual, 66.67, precision_digits=precision),
            0,
        )
