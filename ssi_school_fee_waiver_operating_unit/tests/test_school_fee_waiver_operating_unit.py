# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverOperatingUnit(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the Operating Unit adaptor for ``school_fee_waiver``.

    Covers ``school_fee_waiver`` create/write derivation from the
    selected enrollment's school, the explicit-value-wins contract,
    the negative path of an ambiguous school, and the Operating Unit
    record rule denying list visibility of a document outside a
    restricted user's own Operating Units.
    """

    def test_school_fee_waiver_operating_unit(self):
        """Run every fee waiver Operating Unit adaptor scenario."""
        self.run_yaml_scenario("test_data_school_fee_waiver_operating_unit.yaml")
