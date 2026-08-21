Glue module that adds Operating Unit support to the School Fee Waiver
Deduction module. Extends ``school_fee_waiver_deduction`` with
``mixin.single_operating_unit``. The deduction document's
``operating_unit_id`` is automatically derived from its selected
Waiver, and propagated onto the ``account.move`` journal entry (and
every one of its ``account.move.line``) created when the document is
opened. Adds the matching security group and record rule.
