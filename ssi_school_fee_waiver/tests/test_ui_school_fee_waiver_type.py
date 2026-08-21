# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolFeeWaiverType(HttpSavepointCase):
    """Tour tests for the ``school_fee_waiver_type`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the records required by the edit and delete tours."""
        super().setUpClass()
        cls.rec_edit = cls.env["school_fee_waiver_type"].create(
            {
                "name": "Tour Fee Waiver Type Edit",
                "code": "TOUR-FWT-EDIT",
            }
        )
        cls.rec_delete = cls.env["school_fee_waiver_type"].create(
            {
                "name": "Tour Fee Waiver Type Delete",
                "code": "TOUR-FWT-DEL",
            }
        )

    def test_create(self):
        """Run the create tour for ``school_fee_waiver_type``.

        IK: docs/school_fee_waiver_type/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_school_fee_waiver_type_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_fee_waiver_type``.

        IK: docs/school_fee_waiver_type/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_school_fee_waiver_type_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_fee_waiver_type``.

        IK: docs/school_fee_waiver_type/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_fee_waiver_school_fee_waiver_type_delete",
            login="admin",
        )
