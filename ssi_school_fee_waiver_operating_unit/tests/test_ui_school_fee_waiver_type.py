# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolFeeWaiverType(HttpSavepointCase):
    """Tour test for the Operating Unit field on ``school_fee_waiver_type``
    create.
    """

    @classmethod
    def setUpClass(cls):
        """Grant ``admin`` the multi operating unit group.

        Pre-Condition IK: the Operating Unit field is gated by
        ``groups="operating_unit.group_multi_operating_unit"``.
        """
        super().setUpClass()
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.env.ref("operating_unit.group_multi_operating_unit").sudo().write(
            {"users": [(4, cls.user_admin.id)]}
        )

    def test_create(self):
        """Run the create tour for ``school_fee_waiver_type``.

        IK: docs/school_fee_waiver_type/01-create.md ("Additional
        Fields" delta)
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_operating_unit_school_fee_waiver_type_create",
            login="admin",
        )
