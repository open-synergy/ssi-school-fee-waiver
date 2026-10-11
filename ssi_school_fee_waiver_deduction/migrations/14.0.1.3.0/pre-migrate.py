# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.2.1 -> 14.0.1.3.0
#
# Changes: the Fee Waiver Deduction workflow no longer has the ``open``
#          state (``draft -> confirm -> done``). Every accounting effect
#          now happens when the document reaches ``done``. The
#          ``mixin.transaction_open`` mixin, which declares
#          ``ondelete={"open": "set default"}`` on the ``state``
#          selection, is dropped from the model. Without this
#          pre-migration, Odoo would silently reset every existing
#          ``open`` record to ``draft`` while its journal entry is
#          already posted. The rows are moved to ``done`` BEFORE the
#          module loads, so the selection value is never removed from
#          under a record that still uses it.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Move every ``open`` Fee Waiver Deduction to ``done``.

    Runs in the ``pre`` stage, before the model loses the ``open``
    selection value, so existing posted documents keep their
    accounting effects and become ``done`` (still cancellable).

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates ``school_fee_waiver_deduction.state``
    """
    rows = openupgrade.logged_query(
        env.cr,
        """
        UPDATE school_fee_waiver_deduction
        SET state = 'done'
        WHERE state = 'open'
        """,
    )
    _logger.info(
        "Moved %s Fee Waiver Deduction record(s) from open to done.",
        rows,
    )
