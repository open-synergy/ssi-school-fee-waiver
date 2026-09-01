# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverScheduleVoided(YamlTransactionCase):
    """Scenario-driven tests for Base Amount vs. voided detail lines."""

    def test_school_fee_waiver_schedule_voided(self):
        """Run the Base Amount / voided detail line exclusion scenario.

        Covers Product match and Product Category match with one
        voided detail out of two, a control case with no voided
        detail (Base Amount unchanged), and a term whose only
        matching detail is voided (Base Amount and the capped Amount
        Planned both recompute to zero).
        """
        self.run_yaml_scenario("test_data_school_fee_waiver_schedule_voided.yaml")
