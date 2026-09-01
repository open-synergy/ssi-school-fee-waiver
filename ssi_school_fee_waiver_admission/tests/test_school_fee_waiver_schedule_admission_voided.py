# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolFeeWaiverScheduleAdmissionVoided(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the widened ``_compute_base_amount`` dependencies.

    Covers Base Amount recomputing when a detail line is marked
    ``voided`` *after* the Schedule line already exists, for both
    the Admission-sourced and the Enrollment-sourced path, plus the
    negative path where every matching detail ends up voided.
    """

    def test_school_fee_waiver_schedule_admission_voided(self):
        """Run every Base Amount / voided ``@api.depends`` scenario."""
        self.run_yaml_scenario(
            "test_data_school_fee_waiver_schedule_admission_voided.yaml"
        )
