# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.1.0 -> 14.0.1.1.1
#
# Changes: the shared "Configurator" group for the Fee Waiver Type and
#          Fee Waiver Reason master data
#          (``school_fee_waiver_configurator_group``) is split into two
#          per-model groups, and the module-local category root
#          (``school_fee_waiver_module_category`` and its
#          "Configurator" child, ``school_fee_waiver_configurator_module_category``)
#          is removed in favour of pointing the workflow/data-ownership
#          categories directly at the shared ``ssi_school`` categories.
#          Odoo does not delete a record whose XML ID definition
#          disappears from the module's data files -- it only stops
#          updating it -- so the old shared group and the two obsolete
#          categories would otherwise stay behind as orphans (and the
#          old group would keep granting the now-removed shared
#          access) after a plain module update.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Delete the security records superseded by the split groups.

    Removes the shared configurator group and the two module-local
    category records that no longer exist in this module's data
    files, most dependent record first.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; deletes obsolete ``res.groups`` and
        ``ir.module.category`` records by XML ID
    """
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            "ssi_school_fee_waiver.school_fee_waiver_configurator_group",
            "ssi_school_fee_waiver." "school_fee_waiver_configurator_module_category",
            "ssi_school_fee_waiver.school_fee_waiver_module_category",
        ],
    )
    _logger.info(
        "Deleted the shared Fee Waiver configurator group and the two "
        "obsolete module-local category records."
    )
