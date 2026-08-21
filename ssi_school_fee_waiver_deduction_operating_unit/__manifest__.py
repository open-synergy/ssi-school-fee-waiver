# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "School Fee Waiver Deduction - Operating Unit",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia, "
    "Odoo Community Association (OCA)",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_school_fee_waiver_deduction",
        "ssi_school_fee_waiver_operating_unit",
        "ssi_operating_unit_mixin",
    ],
    "data": [
        "security/res_groups/school_fee_waiver_deduction.xml",
        "security/ir_rule/school_fee_waiver_deduction.xml",
        "views/school_fee_waiver_deduction.xml",
    ],
    "demo": [],
}
