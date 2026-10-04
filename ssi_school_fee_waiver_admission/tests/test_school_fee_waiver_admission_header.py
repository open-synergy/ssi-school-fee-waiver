# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverAdmissionHeader(YamlTransactionCase):
    """Scenario-driven tests for the fee waiver header amounts."""

    def test_school_fee_waiver_admission_header(self):
        """Run the admission header fee waiver scenario.

        Covers an Open waiver, a partially deducted schedule line
        and a Skipped schedule line, checking the fee waiver fields
        and the deduction hooks of the admission.
        """
        self.run_yaml_scenario("test_data_school_fee_waiver_admission_header.yaml")
