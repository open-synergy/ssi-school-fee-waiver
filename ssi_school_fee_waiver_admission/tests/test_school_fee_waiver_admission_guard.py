# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverAdmissionGuard(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Scenario-driven tests for the admission fee waiver guards."""

    def test_school_fee_waiver_admission_guard(self):
        """Run the pre-Open waiver and admission guard scenario.

        Covers a waiver billed against a Draft admission that already
        has a student profile (approved, scheduled, and the admission
        then opened), rejecting Compute Payment while a waiver refers
        to an admission payment term, and rejecting cancellation of an
        admission while a fee waiver is active until every waiver is
        cancelled.
        """
        self.run_yaml_scenario("test_data_school_fee_waiver_admission_guard.yaml")
