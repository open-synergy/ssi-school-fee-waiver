# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverGuard(YamlTransactionCase):
    """Scenario-driven tests for the enrollment fee waiver guards."""

    def test_school_fee_waiver_guard(self):
        """Run the payment term deletion and enrollment cancel scenario.

        Covers rejecting deletion of an enrollment payment term that a
        fee waiver (Single Payment Term) or a Schedule line (Multiple
        Payment Terms) refers to, Compute Payment succeeding while only
        a Schedule-less draft waiver exists and being rejected once a
        waiver refers to a term, and rejecting cancellation of an
        enrollment while a fee waiver is active until every waiver is
        cancelled.
        """
        self.run_yaml_scenario("test_data_school_fee_waiver_guard.yaml")
