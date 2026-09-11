# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverSchedule(YamlTransactionCase):
    """Scenario-driven tests for ``school_fee_waiver_schedule``."""

    def test_school_fee_waiver_schedule(self):
        """Run the schedule generation/compute/action/constraint scenario.

        Covers Single/Multiple Payment Terms generation, matching by
        Product and by Product Category, all three ``computation``
        values, the Max Amount ceiling, idempotent regeneration
        (including after Skip/Cancel), the regenerate guard matching
        pairings by ``_get_source_term()`` -- a Realized line is not
        duplicated and a newly-eligible term still gets scheduled,
        Amount Waived recomputation, the duplicate (Line, Payment
        Term) constraint, the Payment Term ownership constraint, and
        rejection of Skip/Cancel on a Realized line.
        """
        self.run_yaml_scenario("test_data_school_fee_waiver_schedule.yaml")
