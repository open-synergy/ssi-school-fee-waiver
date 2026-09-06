# Auto-Open Fee Waiver Deduction

> **Module:** `ssi_school_fee_waiver_deduction`\
> **Model:** `school_fee_waiver_deduction`\
> **Menu:** School > Fee Waiver > Fee Waiver Deductions\
> **Actor:** System — triggered automatically, no user interaction\
> **State:** `confirm` → `open`\
> **Requires:** `05-approve`

There is no **Start** button on this model: this model sets
`_automatically_insert_open_button = False`, so the mixin never inserts the button in
the first place, and its policy template has no active row for `open_ok`. The transition
to **On Progress** is performed automatically by `action_approve_approval` itself, right
after the last pending approval level is fulfilled.

## Pre-Condition

- **Record:** All approval levels for this document have just been fulfilled (the last
  step of `05-approve`).
- **Record:** Amount Unallocated is zero -- otherwise this transition is rejected with
  an error and the document stays in **Waiting for Approval**.

## Flow

This transition has no click steps — it is triggered automatically by the system as part
of `05-approve`. The last pending approver clicks **Approve**; once every approval level
is fulfilled, the document moves straight to **On Progress** without a separate action.

## Post-Condition

- Status changes to **On Progress**, shown on the statusbar.
- A journal entry is created and posted: one debit line per Deduction Line (to that
  line's own Account), and one credit line on the Receivable Account for the full Amount
  Total.
- The credit line is reconciled against the receivable journal item of every allocated
  invoice, reducing each invoice's own residual amount by its own Allocation Amount. An
  invoice whose residual reaches zero moves to **Paid** on its own.
- Every realized Schedule line (one per Deduction Line) moves to **Realized**, with its
  own Amount Realized filled in and its own Deduction pointing back to this document.
