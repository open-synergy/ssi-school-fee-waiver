# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class SchoolFeeWaiverDeduction(models.Model):
    """Extend School Fee Waiver Deduction with single OU support.

    Restricts each deduction document to one operating unit, and
    derives ``operating_unit_id`` from the selected ``waiver_id`` on
    create/write instead of relying solely on the creating user's
    default operating unit -- the source Waiver has already settled
    that question, and re-deriving it from anywhere else (the user,
    the student, the school) would create a second, divergent source
    of truth.

    Also propagates that same operating unit onto this document's own
    ``account.move`` header when it is opened
    (``_prepare_standard_move``). The header's own credit line and
    every debit line on ``school_fee_waiver_deduction_line`` are
    ``account.move.line`` records created via
    ``mixin.account_move_single_line``; their operating unit is *not*
    set here. ``ssi_financial_accounting_operating_unit`` (installed
    transitively through ``ssi_school_fee_waiver_operating_unit`` ->
    ``ssi_school_operating_unit``) already overrides
    ``account.move.line.create()`` to copy ``operating_unit_id`` from
    ``move_id`` unconditionally, so duplicating that here would only
    create a second place the same value could drift from.
    """

    _name = "school_fee_waiver_deduction"
    _inherit = [
        "school_fee_waiver_deduction",
        "mixin.single_operating_unit",
    ]

    @api.model
    def create(self, vals):
        """Derive ``operating_unit_id`` from the selected Waiver.

        Overridden so ``operating_unit_id`` always reflects the
        selected Waiver's own operating unit rather than the creating
        user's default operating unit from
        ``mixin.single_operating_unit``, unless the caller explicitly
        passes ``operating_unit_id`` in the same ``vals``.

        :param vals: values for the new record
        :return: the created ``school_fee_waiver_deduction`` record
        """
        self._derive_operating_unit_from_waiver(vals)
        return super().create(vals)

    def write(self, vals):
        """Re-derive ``operating_unit_id`` when ``waiver_id`` changes.

        Only triggers when ``waiver_id`` is part of ``vals``, so a
        write that only sets ``operating_unit_id`` passes through
        unchanged.

        :param vals: values to write
        :return: True
        """
        self._derive_operating_unit_from_waiver(vals)
        return super().write(vals)

    def _derive_operating_unit_from_waiver(self, vals):
        """Mutate ``vals`` in place, deriving ``operating_unit_id``.

        Applies only when ``waiver_id`` is present in ``vals`` and the
        caller has not already supplied ``operating_unit_id``
        explicitly in the same ``vals`` -- an explicit value always
        wins. A Waiver without its own operating unit leaves ``vals``
        untouched, without raising -- the mixin's own default (or an
        explicit value) then applies instead.

        :param vals: the ``create``/``write`` values dict, mutated in
            place
        :return: None
        """
        if "waiver_id" not in vals or "operating_unit_id" in vals:
            return
        waiver = self.env["school_fee_waiver"].browse(vals["waiver_id"])
        if waiver.operating_unit_id:
            vals["operating_unit_id"] = waiver.operating_unit_id.id

    @api.onchange("waiver_id")
    def onchange_operating_unit_id(self):
        """Set ``operating_unit_id`` from the selected Waiver.

        Mirrors the ``create``/``write`` derivation so the form shows
        the correct operating unit as soon as a Waiver is selected.
        Only sets a value when the Waiver has one; otherwise the
        current value is left untouched.
        """
        if self.waiver_id and self.waiver_id.operating_unit_id:
            self.operating_unit_id = self.waiver_id.operating_unit_id

    @api.constrains("operating_unit_id", "waiver_id")
    def _check_operating_unit_matches_waiver(self):
        """Reject an operating unit that diverges from the Waiver's own.

        Only checked when both this document's and the Waiver's own
        ``operating_unit_id`` are set -- a Waiver without one is not a
        conflict, it simply has nothing to compare against.

        :raises ValidationError: when ``operating_unit_id`` differs
            from ``waiver_id.operating_unit_id``.
        """
        for record in self:
            waiver_ou = record.waiver_id.operating_unit_id
            if (
                record.operating_unit_id
                and waiver_ou
                and record.operating_unit_id != waiver_ou
            ):
                error_message = """
Document Type: %s
Context: Configure deduction
Database ID: %s
Problem: Operating Unit '%s' differs from Waiver's own Operating Unit '%s'
Solution: Select the same Operating Unit as the source Waiver
""" % (
                    record._description,
                    record.id,
                    record.operating_unit_id.display_name,
                    waiver_ou.display_name,
                )
                raise ValidationError(_(error_message))

    def _prepare_standard_move(self):
        """Add this document's operating unit to the ``account.move``.

        Guarded by field existence rather than a hard dependency:
        this module does not depend on
        ``ssi_financial_accounting_operating_unit`` directly (only
        transitively, through ``ssi_school_fee_waiver_operating_unit``
        -> ``ssi_school_operating_unit``), so ``account.move`` may not
        carry ``operating_unit_id`` at all in an installation that
        skips that chain.

        :return: dict of ``account.move`` values
        """
        res = super()._prepare_standard_move()
        if "operating_unit_id" in self.env["account.move"]._fields:
            res["operating_unit_id"] = self.operating_unit_id.id
        return res
