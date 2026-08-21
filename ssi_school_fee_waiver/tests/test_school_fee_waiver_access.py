# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverAccess(YamlTransactionCase):
    """Scenario tests for access to the Fee Waiver configurator group.

    Kept separate from the CRUD scenarios of ``school_fee_waiver_type``
    and ``school_fee_waiver_reason`` because it exercises a different
    actor (a user without the configurator group) rather than the
    happy-path configurator.
    """

    def test_school_fee_waiver_access(self):
        """Run the no-configurator-group negative scenarios."""
        self.run_yaml_scenario("test_data_school_fee_waiver_access.yaml")
