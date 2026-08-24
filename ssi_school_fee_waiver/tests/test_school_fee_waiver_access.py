# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverAccess(YamlTransactionCase):
    """Scenario tests for the Fee Waiver Type/Reason configurator groups.

    Kept separate from the CRUD scenarios of ``school_fee_waiver_type``
    and ``school_fee_waiver_reason`` because it exercises different
    actors: a user with no configurator group at all, and a user with
    only one of the two split configurator groups.
    """

    def test_school_fee_waiver_access(self):
        """Run the split-configurator-group access scenarios.

        Covers both the outsider negative path (no configurator group
        at all) and the type/reason separation: a user holding only
        ``school_fee_waiver_type_group`` can manage Fee Waiver Types
        but is rejected on Fee Waiver Reason.
        """
        self.run_yaml_scenario("test_data_school_fee_waiver_access.yaml")
