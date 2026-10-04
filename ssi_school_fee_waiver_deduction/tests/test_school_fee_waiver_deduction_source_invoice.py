# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverDeductionSourceInvoice(YamlTransactionCase):
    """Scenario tests for the Allocation source-invoice rule."""

    def test_school_fee_waiver_deduction_source_invoice(self):
        """Run the source-invoice restriction scenario."""
        self.run_yaml_scenario(
            "test_data_school_fee_waiver_deduction_source_invoice.yaml"
        )
