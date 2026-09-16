# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverDeductionMultiAllocation(YamlTransactionCase):
    """Scenario tests for multi-Allocation reconciliation."""

    def test_school_fee_waiver_deduction_multi_allocation(self):
        """Run the multi-Allocation partial/full reconcile scenario."""
        self.run_yaml_scenario(
            "test_data_school_fee_waiver_deduction_multi_allocation.yaml"
        )
