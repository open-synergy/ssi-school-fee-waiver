# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


# Adds the fee waiver deduction rule to the cross-module force-delete
# guard ``_check_force_delete_allowed`` (contract K1 of ``ssi_school``).
class CustomerInvoice(models.Model):
    _name = "customer_invoice"
    _inherit = [
        "customer_invoice",
    ]

    def _check_force_delete_allowed(self):
        """Reject a force delete of an invoice a deduction allocation uses.

        Extends the K1 guard of ``ssi_school``: calls ``super()`` first,
        then rejects the invoice when any
        ``school_fee_waiver_deduction_allocation`` points to it, whatever
        the state of the deduction document, because the
        ``ondelete="restrict"`` reference would still block the delete.
        Read-only: it never writes.

        :raises UserError: when a fee waiver deduction allocation
            references this invoice
        :return: None
        """
        super()._check_force_delete_allowed()
        self.ensure_one()
        allocation = (
            self.env["school_fee_waiver_deduction_allocation"]
            .sudo()
            .search(
                [("customer_invoice_id", "=", self.id)],
                limit=1,
            )
        )
        if allocation:
            error_message = (
                _(
                    """
Context: Force delete customer invoice
Database ID: %s
Problem: Invoice is referenced by fee waiver deduction allocation '%s' of deduction '%s'
Solution: Remove the allocation from the fee waiver deduction document first
"""
                )
                % (
                    self.id,
                    allocation.display_name,
                    allocation.deduction_id.display_name,
                )
            )
            raise UserError(error_message)
