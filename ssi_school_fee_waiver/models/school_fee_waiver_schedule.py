# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SchoolFeeWaiverSchedule(models.Model):
    """
    Represents one realization term of a waiver Line.
    A schedule line pins down exactly which payment term a waiver
    Line applies to, how much of the billing component it covers
    (``base_amount``, matched from the linked payment term's detail
    lines), and how much this waiver plans to waive in that term
    (``amount_planned``). A later, out-of-scope module realizes a
    schedule line by posting the actual deduction and filling
    ``amount_realized``.
    """

    _name = "school_fee_waiver_schedule"
    _description = "School Fee Waiver Schedule"
    _order = "date, line_id, id"

    line_id = fields.Many2one(
        string="Line",
        comodel_name="school_fee_waiver_line",
        required=True,
        ondelete="cascade",
        help="Waiver line this schedule line realizes one term of.",
    )
    waiver_id = fields.Many2one(
        string="Waiver",
        comodel_name="school_fee_waiver",
        related="line_id.waiver_id",
        store=True,
        help="Fee waiver of the linked Line, kept as a stored column "
        "so this model's own domains and record rules do not have to "
        "traverse through Line.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="waiver_id.company_currency_id",
        store=True,
        compute_sudo=True,
        help="Currency the Base Amount, Amount Planned, and Amount "
        "Realized fields are expressed in, following the waiver's "
        "Company Currency.",
    )
    payment_term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="school_enrollment_payment_term",
        ondelete="restrict",
        help="Payment term this schedule line realizes. Left as a "
        "plain, non-required field so an extension module can give "
        "this model its own further source field instead -- see "
        "``_get_source_term``.",
    )
    date = fields.Date(
        string="Date",
        required=True,
        help="Date this waiver is due to take effect: the linked "
        "payment term's Estimated Due Date.",
    )
    base_amount = fields.Monetary(
        string="Base Amount",
        currency_field="currency_id",
        compute="_compute_base_amount",
        store=True,
        compute_sudo=True,
        help="Billing amount this schedule line's Computation is "
        "applied to: the sum of the linked payment term's detail "
        "lines matching the Line's Product, or its Product Category "
        "when the Line targets one. Zero when no payment term is "
        "linked.",
    )
    amount_planned = fields.Monetary(
        string="Amount Planned",
        currency_field="currency_id",
        compute="_compute_amount_planned",
        store=True,
        compute_sudo=True,
        help="Amount this schedule line plans to waive: the Line's "
        "Percentage of Base Amount, its Fixed Amount, or the full "
        "Base Amount, capped at the Line's Max Amount when that "
        "ceiling is above zero, and never above Base Amount.",
    )
    amount_realized = fields.Monetary(
        string="Amount Realized",
        currency_field="currency_id",
        default=0.0,
        readonly=True,
        help="Amount actually waived for this schedule line. Filled "
        "by the deduction document, a later module out of this "
        "item's scope; always zero until then.",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("scheduled", "Scheduled"),
            ("realized", "Realized"),
            ("skipped", "Skipped"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        required=True,
        help="Lifecycle of this schedule line. Deliberately a plain "
        "stored field, not computed: moving a line to Skipped is a "
        "human decision the system cannot infer on its own.",
    )
    note = fields.Char(
        string="Note",
        help="Free-form note about this schedule line.",
    )

    def _get_source_term(self):
        """Return the payment term this schedule line realizes.

        Extension point: a module that gives Schedule its own extra
        source field (alongside ``payment_term_id``) overrides this
        to return that field instead.

        :return: ``school_enrollment_payment_term`` record, or an
            empty recordset when unset
        """
        self.ensure_one()
        return self.payment_term_id

    def _get_source_term_parent(self):
        """Return the billing source record owning the source term.

        Used by ``_check_payment_term_source`` to compare against the
        waiver's own ``_get_source_record()``, so that check stays
        meaningful for whatever billing source an extension module
        introduces.

        :return: recordset of the source term's parent (e.g. its
            ``school_enrollment``), possibly empty
        """
        self.ensure_one()
        return self.payment_term_id.enrollment_id

    @api.depends(
        "payment_term_id",
        "payment_term_id.detail_ids.price_subtotal",
        "payment_term_id.detail_ids.product_id",
        "payment_term_id.detail_ids.product_id.categ_id",
        "line_id.product_id",
        "line_id.product_category_id",
    )
    def _compute_base_amount(self):
        """Sum the source term's detail lines matching the Line's scope.

        Matches by the detail lines' own ``product_id`` when the Line
        has a Product, or by their ``product_id.categ_id`` when the
        Line targets a Product Category instead.

        :return: nothing; assigns ``base_amount``
        """
        for record in self:
            result = 0.0
            term = record._get_source_term()
            line = record.line_id
            if term:
                if line.product_category_id:
                    details = term.detail_ids.filtered(
                        lambda detail: detail.product_id.categ_id
                        == line.product_category_id
                    )
                else:
                    details = term.detail_ids.filtered(
                        lambda detail: detail.product_id == line.product_id
                    )
                result = sum(details.mapped("price_subtotal"))
            record.base_amount = result

    @api.depends(
        "base_amount",
        "line_id.computation",
        "line_id.percentage",
        "line_id.amount_fixed",
        "line_id.max_amount",
    )
    def _compute_amount_planned(self):
        """Apply the Line's Computation to the Base Amount.

        The raw computed value is then capped at ``base_amount``
        (unconditionally), and again at the Line's ``max_amount``
        when that ceiling is above zero.

        :return: nothing; assigns ``amount_planned``
        """
        for record in self:
            line = record.line_id
            if line.computation == "percentage":
                result = record.base_amount * line.percentage / 100.0
            elif line.computation == "fixed":
                result = line.amount_fixed
            else:
                result = record.base_amount
            result = min(result, record.base_amount)
            if line.max_amount > 0.0:
                result = min(result, line.max_amount)
            record.amount_planned = result

    @api.constrains("line_id", "payment_term_id")
    def _check_duplicate_line_payment_term(self):
        """Forbid two schedule lines sharing Line and Payment Term.

        :raises ValidationError: when another schedule line of the
            same Line already uses the same Payment Term.
        """
        for record in self:
            term = record._get_source_term()
            if not term:
                continue
            duplicate_count = self.search_count(
                [
                    ("id", "!=", record.id),
                    ("line_id", "=", record.line_id.id),
                    ("payment_term_id", "=", term.id),
                ]
            )
            if duplicate_count > 0:
                error_message = """
Document Type: %s
Context: Configure waiver schedule
Database ID: %s
Problem: Payment Term '%s' is already scheduled for this Line
Solution: Select a Payment Term not yet scheduled for this Line
""" % (
                    record._description,
                    record.id,
                    term.display_name,
                )
                raise ValidationError(_(error_message))

    @api.constrains("payment_term_id", "waiver_id")
    def _check_payment_term_source(self):
        """Require the source term to belong to the waiver's source.

        Rewritten through ``_get_source_term``/``_get_source_term_parent``
        and the waiver's own ``_get_source_record`` so this check
        keeps working for whatever billing source an extension module
        adds, without renaming this method or its XML ID references.

        :raises ValidationError: when the source term's parent record
            is set and differs from the waiver's own billing source
            record.
        """
        for record in self:
            term = record._get_source_term()
            parent = record._get_source_term_parent()
            waiver = record.waiver_id
            source = waiver._get_source_record() if waiver else waiver
            if term and parent and parent != source:
                error_message = """
Document Type: %s
Context: Configure waiver schedule
Database ID: %s
Problem: Payment Term '%s' does not belong to the waiver's billing source
Solution: Select a Payment Term of the waiver's own billing source
""" % (
                    record._description,
                    record.id,
                    term.display_name,
                )
                raise ValidationError(_(error_message))

    def action_skip(self):
        """Move the selected schedule lines to Skipped."""
        for record in self.sudo():
            record._skip()

    def _skip(self):
        """Move this schedule line to Skipped.

        :raises UserError: when this line is not in ``draft`` or
            ``scheduled``.
        :return: nothing; writes ``state``
        """
        self.ensure_one()
        self._check_skip_cancel_allowed("Skip", "skipped")
        self.write({"state": "skipped"})

    def action_cancel_schedule(self):
        """Move the selected schedule lines to Cancelled."""
        for record in self.sudo():
            record._cancel_schedule()

    def _cancel_schedule(self):
        """Move this schedule line to Cancelled.

        :raises UserError: when this line is not in ``draft`` or
            ``scheduled``.
        :return: nothing; writes ``state``
        """
        self.ensure_one()
        self._check_skip_cancel_allowed("Cancel", "cancelled")
        self.write({"state": "cancelled"})

    def _check_skip_cancel_allowed(self, action_label, past_tense):
        """Guard Skip/Cancel to schedule lines still Draft or Scheduled.

        :param action_label: human-readable action name used in the
            error message ("Skip" or "Cancel")
        :param past_tense: past-tense form of ``action_label``, used
            in the error message ("skipped" or "cancelled")
        :raises UserError: when this line's state is not ``draft`` or
            ``scheduled`` (in particular, ``realized``).
        :return: nothing
        """
        self.ensure_one()
        if self.state not in ("draft", "scheduled"):
            error_message = """
Document Type: %s
Context: %s waiver schedule line
Database ID: %s
Problem: Schedule line is in state '%s', not Draft or Scheduled
Solution: Only a Draft or Scheduled schedule line may be %s
""" % (
                self._description,
                action_label,
                self.id,
                self.state,
                past_tense,
            )
            raise UserError(_(error_message))
