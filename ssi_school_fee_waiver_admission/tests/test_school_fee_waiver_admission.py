# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverAdmission(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the Admission billing source for ``school_fee_waiver``.

    Covers ``school_fee_waiver`` creation with Billing Source
    Admission (School/Grade/Academic Year/Partner derivation,
    multi-term Schedule generation against
    ``school_admission_payment_term`` for Percentage/Fixed/Full
    computations), the Enrollment path regression, and every
    Admission-specific negative path.
    """

    def test_school_fee_waiver_admission(self):
        """Run every Fee Waiver Admission billing source scenario."""
        self.run_yaml_scenario("test_data_school_fee_waiver_admission.yaml")
