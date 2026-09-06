# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "School Fee Waiver Deduction",
    "version": "14.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    # pylint: disable=line-too-long
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia, Odoo Community Association (OCA)",  # noqa: B950
    # pylint: enable=line-too-long
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_school_fee_waiver",
        "ssi_customer_invoice",
        "ssi_accounting_entry_mixin",
        "ssi_company_currency_mixin",
        "web_tour",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_groups/school_fee_waiver_deduction.xml",
        "security/ir_model_access/school_fee_waiver_deduction.xml",
        "security/ir_model_access/school_fee_waiver_deduction_line.xml",
        "security/ir_model_access/school_fee_waiver_deduction_allocation.xml",
        "security/ir_rule/school_fee_waiver_deduction.xml",
        "ir_sequence/school_fee_waiver_deduction.xml",
        "sequence_template/school_fee_waiver_deduction.xml",
        "approval_template/school_fee_waiver_deduction.xml",
        "policy_template/school_fee_waiver_deduction.xml",
        "menu.xml",
        "views/school_fee_waiver_deduction.xml",
        "views/school_fee_waiver_type.xml",
        "views/school_fee_waiver_schedule.xml",
        "views/assets.xml",
    ],
}
