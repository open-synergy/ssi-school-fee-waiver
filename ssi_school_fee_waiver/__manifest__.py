# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "School Fee Waiver",
    "version": "14.0.1.1.1",
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
        "ssi_school",
        "ssi_master_data_mixin",
        "ssi_m2o_configurator_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_open_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_company_currency_mixin",
        "ssi_localdict_mixin",
        "web_tour",
    ],
    "data": [
        "security/ir_module_category/school_fee_waiver.xml",
        "security/res_groups/school_fee_waiver_configurator.xml",
        "security/res_groups/school_fee_waiver.xml",
        "security/ir_model_access/school_fee_waiver_type.xml",
        "security/ir_model_access/school_fee_waiver_reason.xml",
        "security/ir_model_access/school_fee_waiver.xml",
        "security/ir_model_access/school_fee_waiver_line.xml",
        "security/ir_model_access/school_fee_waiver_schedule.xml",
        "security/ir_rule/school_fee_waiver.xml",
        "ir_sequence/school_fee_waiver.xml",
        "sequence_template/school_fee_waiver.xml",
        "approval_template/school_fee_waiver.xml",
        "policy_template/school_fee_waiver.xml",
        "menu.xml",
        "views/school_fee_waiver_type.xml",
        "views/school_fee_waiver_reason.xml",
        "views/school_fee_waiver.xml",
        "views/assets.xml",
    ],
}
