# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverDeductionOperatingUnit(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the Operating Unit adaptor for ``school_fee_waiver_deduction``.

    Covers create/write derivation of ``operating_unit_id`` from the
    selected Waiver, the explicit-value-wins contract, propagation
    onto the resulting ``account.move`` and its lines once the
    document is opened, the Operating Unit record rule denying list
    visibility of a document outside a restricted user's own
    Operating Units, and the negative path of an operating unit that
    diverges from the source Waiver's own.
    """

    def test_school_fee_waiver_deduction_operating_unit(self):
        """Run every deduction Operating Unit adaptor scenario."""
        self.run_yaml_scenario(
            "test_data_school_fee_waiver_deduction_operating_unit.yaml"
        )
