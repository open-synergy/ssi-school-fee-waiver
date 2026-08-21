# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiver(YamlTransactionCase):
    """Scenario-driven tests for the ``school_fee_waiver`` document."""

    def test_school_fee_waiver(self):
        """Run the ``school_fee_waiver`` create/workflow/constraint scenario.

        Covers create + computed field derivation, the full
        Draft -> Confirm -> Approve -> Open -> Done workflow, Cancel
        via the cancel-reason wizard, and every ``@api.constrains`` on
        ``school_fee_waiver`` and ``school_fee_waiver_line``, plus
        rejection of an approval attempt by a user with no approver
        group.
        """
        self.run_yaml_scenario("test_data_school_fee_waiver.yaml")
