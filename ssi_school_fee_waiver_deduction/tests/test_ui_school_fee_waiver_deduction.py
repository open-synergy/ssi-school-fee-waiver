# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolFeeWaiverDeduction(HttpSavepointCase):
    """Tour tests for the ``school_fee_waiver_deduction`` instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the master data and deductions required by the tours.

        Every tour scenario gets its own dedicated Student/Enrollment/
        Waiver/Schedule/Invoice chain (suffixed CREATE/CONFIRM/APPROVE/
        REJECT/FINISH/CANCEL/RESTART/RAPPROVAL), the same pattern
        ``ssi_school_fee_waiver``'s own ``test_ui_school_fee_waiver.py``
        uses -- so the list view always shows one uniquely-named row per
        scenario (searchable by the Student column) and so a tour that
        actually opens its own document (Approve/Finish) can never
        realize a Schedule line or reconcile an invoice shared by
        another scenario's fixture.
        """
        super().setUpClass()
        admin = cls.env.ref("base.user_admin")

        # ── Shared academic/accounting infrastructure ────────────────
        grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR FWD Grade Type", "code": "TOURFWDGT"}
        )
        school = cls.env["school"].create(
            {
                "name": "TOUR FWD School",
                "code": "TOURFWDSC",
                "grade_type_id": grade_type.id,
            }
        )
        academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR FWD Academic Year",
                "code": "TOURFWDAY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR FWD Academic Term",
                "code": "TOURFWDTM",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR FWD Grade",
                "code": "TOURFWDGR",
                "type_id": grade_type.id,
            }
        )
        grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR FWD Grade Class",
                "code": "TOURFWDGC",
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )

        account_type_income = cls.env.ref("account.data_account_type_revenue")
        account_type_receivable = cls.env.ref("account.data_account_type_receivable")
        account_type_expense = cls.env.ref("account.data_account_type_expenses")
        income_account = cls.env["account.account"].create(
            {
                "name": "TOUR FWD Income Account",
                "code": "TOURFWDIA",
                "user_type_id": account_type_income.id,
                "reconcile": False,
            }
        )
        cls.receivable_account = cls.env["account.account"].create(
            {
                "name": "TOUR FWD Receivable Account",
                "code": "TOURFWDRA",
                "user_type_id": account_type_receivable.id,
                "reconcile": True,
            }
        )
        cls.discount_account = cls.env["account.account"].create(
            {
                "name": "TOUR FWD Discount Account",
                "code": "TOURFWDDA",
                "user_type_id": account_type_expense.id,
                "reconcile": False,
            }
        )
        cls.deduction_journal = cls.env["account.journal"].create(
            {
                "name": "TOUR FWD Deduction Journal",
                "code": "TOURFWDDJ",
                "type": "general",
            }
        )
        sale_journal = cls.env["account.journal"].create(
            {
                "name": "TOUR FWD Sale Journal",
                "code": "TOURFWDSJ",
                "type": "sale",
            }
        )
        product = cls.env["product.product"].create(
            {"name": "TOUR FWD Product", "type": "service"}
        )
        waiver_type = cls.env["school_fee_waiver_type"].create(
            {
                "name": "TOUR FWD Type",
                "code": "TOURFWDTY",
                "deduction_journal_id": cls.deduction_journal.id,
                "discount_account_id": cls.discount_account.id,
            }
        )
        waiver_reason = cls.env["school_fee_waiver_reason"].create(
            {"name": "TOUR FWD Reason", "code": "TOURFWDRS"}
        )
        invoice_type = cls.env["customer_invoice_type"].create(
            {
                "name": "TOUR FWD Invoice Type",
                "code": "/",
                "journal_id": sale_journal.id,
                "receivable_account_id": cls.receivable_account.id,
            }
        )
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR FWD Cancel Reason",
                "code": "TOURFWDCR",
                # The cancel wizard's radio widget only lists reasons in
                # ir.model.all_cancel_reason_ids, which merges
                # model-specific links with every global_use=True
                # reason. Without this, the tour's radio option never
                # renders.
                "global_use": True,
            }
        )

        def build_open_waiver(suffix, price):
            """Build a dedicated Student/Enrollment/Waiver, then open it.

            :param suffix: unique code/name suffix for this scenario
            :param price: ``price_unit`` of the term's single detail
                line, and so the resulting Schedule line's own Amount
                Planned (Computation is Full Coverage)
            :return: ``(contact, waiver, schedule)`` -- the billed
                Partner, the opened Waiver, and its single Schedule
                line generated on Open
            """
            contact = cls.env["res.partner"].create(
                {"name": "TOUR FWD Contact " + suffix}
            )
            student = cls.env["school_student"].create(
                {
                    "name": "TOUR FWD Student " + suffix,
                    "code": "TFWDST" + suffix,
                    "contact_id": contact.id,
                    "school_id": school.id,
                }
            )
            enrollment = cls.env["school_enrollment"].create(
                {
                    "academic_year_id": academic_year.id,
                    "academic_term_id": academic_term.id,
                    "school_id": school.id,
                    "grade_id": grade.id,
                    "grade_class_id": grade_class.id,
                    "student_id": student.id,
                }
            )
            term = cls.env["school_enrollment_payment_term"].create(
                {
                    "enrollment_id": enrollment.id,
                    "name": "TOUR FWD Term " + suffix,
                    "date_due": "2026-08-15",
                    "detail_ids": [
                        (
                            0,
                            0,
                            {
                                "product_id": product.id,
                                "name": "TOUR FWD Term " + suffix + " Fee",
                                "account_id": income_account.id,
                                "uom_quantity": 1.0,
                                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                                "price_unit": price,
                            },
                        )
                    ],
                }
            )
            waiver = cls.env["school_fee_waiver"].create(
                {
                    "type_id": waiver_type.id,
                    "reason_id": waiver_reason.id,
                    "student_id": student.id,
                    "enrollment_id": enrollment.id,
                    "coverage": "single_term",
                    "payment_term_id": term.id,
                    "user_id": admin.id,
                    "line_ids": [
                        (0, 0, {"product_id": product.id, "computation": "full"})
                    ],
                }
            )
            waiver = waiver.with_user(admin)
            waiver.action_confirm()
            waiver.invalidate_cache()
            waiver.action_approve_approval()
            schedule = waiver.schedule_ids
            return contact, waiver, schedule

        def build_open_invoice(partner, price):
            """Create and open a customer invoice for ``partner``.

            :param partner: ``res.partner`` billed
            :param price: ``price_unit`` of the invoice's own line
            :return: the opened ``customer_invoice``
            """
            invoice = cls.env["customer_invoice"].create(
                {
                    "type_id": invoice_type.id,
                    "partner_id": partner.id,
                    "date": "2026-08-20",
                    "date_due": "2026-09-20",
                    "currency_id": cls.env.company.currency_id.id,
                    "journal_id": sale_journal.id,
                    "receivable_account_id": cls.receivable_account.id,
                }
            )
            cls.env["customer_invoice.line"].create(
                {
                    "customer_invoice_id": invoice.id,
                    "name": "Line",
                    "account_id": income_account.id,
                    "uom_quantity": 1,
                    "price_unit": price,
                }
            )
            invoice = invoice.with_user(admin)
            invoice.action_confirm()
            invoice.invalidate_cache()
            invoice.action_approve_approval()
            return invoice

        def build_deduction(suffix, price):
            """Build a draft deduction fully filled for ``suffix``.

            :param suffix: unique code/name suffix for this scenario
            :param price: amount used for both the Line and the
                Allocation (they match, so Amount Unallocated is zero
                and the document is ready to Open)
            :return: the draft ``school_fee_waiver_deduction``
            """
            contact, waiver, schedule = build_open_waiver(suffix, price)
            invoice = build_open_invoice(contact, price)
            return cls.env["school_fee_waiver_deduction"].create(
                {
                    "waiver_id": waiver.id,
                    "journal_id": cls.deduction_journal.id,
                    "receivable_account_id": cls.receivable_account.id,
                    "line_ids": [
                        (
                            0,
                            0,
                            {
                                "schedule_id": schedule.id,
                                "account_id": cls.discount_account.id,
                                "amount": price,
                            },
                        )
                    ],
                    "allocation_ids": [
                        (
                            0,
                            0,
                            {"customer_invoice_id": invoice.id, "amount": price},
                        )
                    ],
                }
            )

        # ── Pre-Condition for 04-confirm -- a Draft deduction, fully
        # filled, ready for the tour to click Confirm. ─────────────────
        cls.tour_deduction_confirm = build_deduction("CONFIRM", 500000.0)

        # ── Pre-Condition for 05-approve -- already pushed to Waiting
        # for Approval, ready for the tour to click Approve for real. ──
        cls.tour_deduction_approve = build_deduction("APPROVE", 1000000.0)
        cls.tour_deduction_approve = cls.tour_deduction_approve.with_user(admin)
        cls.tour_deduction_approve.action_confirm()
        cls.tour_deduction_approve.invalidate_cache()

        # ── Pre-Condition for 06-reject -- same shape as 05-approve,
        # own Schedule/invoice so approving one never touches the
        # other's fixture. ──────────────────────────────────────────
        cls.tour_deduction_reject = build_deduction("REJECT", 500000.0)
        cls.tour_deduction_reject = cls.tour_deduction_reject.with_user(admin)
        cls.tour_deduction_reject.action_confirm()
        cls.tour_deduction_reject.invalidate_cache()

        # ── Pre-Condition for 09-finish -- already On Progress, same
        # recipe as 05-approve's own fixture, its own Schedule/invoice.
        cls.tour_deduction_finish = build_deduction("FINISH", 1000000.0)
        cls.tour_deduction_finish = cls.tour_deduction_finish.with_user(admin)
        cls.tour_deduction_finish.action_confirm()
        cls.tour_deduction_finish.invalidate_cache()
        cls.tour_deduction_finish.action_approve_approval()

        # ── Pre-Condition for 10-cancel -- a header-only Draft
        # deduction. Cancel from Draft does not require any Line, so no
        # Schedule/invoice fixture is needed at all. ────────────────────
        cancel_contact, cancel_waiver, _cancel_schedule = build_open_waiver(
            "CANCEL", 500000.0
        )
        cls.tour_deduction_cancel = cls.env["school_fee_waiver_deduction"].create(
            {
                "waiver_id": cancel_waiver.id,
                "journal_id": cls.deduction_journal.id,
                "receivable_account_id": cls.receivable_account.id,
            }
        )

        # ── Pre-Condition for 12-restart -- already Cancelled. Written
        # directly rather than through the wizard, since the cancel
        # mechanism itself is exercised by 10-cancel.md's own tour. ────
        restart_contact, restart_waiver, _restart_schedule = build_open_waiver(
            "RESTART", 500000.0
        )
        cls.tour_deduction_restart = cls.env["school_fee_waiver_deduction"].create(
            {
                "waiver_id": restart_waiver.id,
                "journal_id": cls.deduction_journal.id,
                "receivable_account_id": cls.receivable_account.id,
            }
        )
        cls.tour_deduction_restart.write({"state": "cancel"})

        # ── Pre-Condition for 14-restart-approval -- Waiting for
        # Approval, same recipe as 06-reject. ───────────────────────────
        cls.tour_deduction_restart_approval = build_deduction("RAPPROVAL", 500000.0)
        cls.tour_deduction_restart_approval = (
            cls.tour_deduction_restart_approval.with_user(admin)
        )
        cls.tour_deduction_restart_approval.action_confirm()
        cls.tour_deduction_restart_approval.invalidate_cache()

        # ── Dedicated CREATE waiver/invoice -- the 01-create tour picks
        # Waiver, Schedule, and Customer Invoice through the browser, so
        # each of those dropdowns must resolve to exactly one candidate.
        # The Waiver's own sequence-assigned number is unpredictable, so
        # it is overwritten with a fixed, searchable name below. ────────
        create_contact, create_waiver, _create_schedule = build_open_waiver(
            "CREATE", 1000000.0
        )
        create_waiver.sudo().write({"name": "TOUR-FWD-WAIVER-CREATE"})
        cls.create_invoice = build_open_invoice(create_contact, 1000000.0)

    def test_create(self):
        """Run the create tour for ``school_fee_waiver_deduction``.

        IK: docs/school_fee_waiver_deduction/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_deduction_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``school_fee_waiver_deduction``.

        IK: docs/school_fee_waiver_deduction/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_deduction_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``school_fee_waiver_deduction``.

        IK: docs/school_fee_waiver_deduction/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_deduction_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``school_fee_waiver_deduction``.

        IK: docs/school_fee_waiver_deduction/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_deduction_reject",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour for ``school_fee_waiver_deduction``.

        IK: docs/school_fee_waiver_deduction/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_deduction_finish",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_fee_waiver_deduction``.

        IK: docs/school_fee_waiver_deduction/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_deduction_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``school_fee_waiver_deduction``.

        IK: docs/school_fee_waiver_deduction/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_deduction_restart",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval tour for ``school_fee_waiver_deduction``.

        IK: docs/school_fee_waiver_deduction/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_deduction_restart_approval",
            login="admin",
        )
