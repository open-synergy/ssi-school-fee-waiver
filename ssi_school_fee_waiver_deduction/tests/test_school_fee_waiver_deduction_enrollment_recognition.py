# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverDeductionEnrollmentRecognition(YamlTransactionCase):
    """Scenario tests for deferring a deduction to enrollment recognition."""

    def test_school_fee_waiver_deduction_enrollment_recognition(self):
        """Run the Enrollment Revenue Recognition deferral scenario."""
        self.run_yaml_scenario(
            "test_data_school_fee_waiver_deduction_enrollment_recognition.yaml"
        )
