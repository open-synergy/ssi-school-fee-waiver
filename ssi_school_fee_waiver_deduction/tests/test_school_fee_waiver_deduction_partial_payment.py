# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverDeductionPartialPayment(YamlTransactionCase):
    """Cancelling a Deduction on an already partially-paid invoice."""

    def test_school_fee_waiver_deduction_partial_payment(self):
        """Run the partial-payment + Deduction cancel scope scenario."""
        self.run_yaml_scenario(
            "test_data_school_fee_waiver_deduction_partial_payment.yaml"
        )
