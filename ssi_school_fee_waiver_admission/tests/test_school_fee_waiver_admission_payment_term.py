# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverAdmissionPaymentTerm(YamlTransactionCase):
    """Scenario-driven tests for the admission payment term amounts."""

    def test_school_fee_waiver_admission_payment_term(self):
        """Run the admission payment term fee waiver amount scenario.

        Covers an Open waiver with nothing deducted, a fully and a
        partially deducted schedule line, and a Skipped schedule
        line, checking the four ``fee_waiver_amount*`` fields.
        """
        self.run_yaml_scenario(
            "test_data_school_fee_waiver_admission_payment_term.yaml"
        )
