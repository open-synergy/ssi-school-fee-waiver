# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverReason(YamlTransactionCase):
    """Scenario tests for ``school_fee_waiver_reason``."""

    def test_school_fee_waiver_reason(self):
        """Run the CRUD and negative-path scenarios for the reason."""
        self.run_yaml_scenario("test_data_school_fee_waiver_reason.yaml")
