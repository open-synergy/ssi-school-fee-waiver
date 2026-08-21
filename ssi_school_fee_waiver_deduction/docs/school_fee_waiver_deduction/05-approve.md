# Approve Fee Waiver Deduction

> **Module:** ssi_school_fee_waiver_deduction\
> **Model:** `school_fee_waiver_deduction`\
> **Menu:** School > Fee Waiver > Fee Waiver Deductions\
> **Actor:** approver on the pending approval level\
> **State:** `confirm` → `open`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Record:** Amount Unallocated is zero -- the full Amount Total has been assigned
  across the Allocation lines.
- **Config:** An active `policy.template` grants `approve_ok` to the actor's group.
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**.

## Flow

1. Open the **School > Fee Waiver > Fee Waiver Deductions** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, status changes automatically to **On Progress**,
  shown on the statusbar, and the record's **# Document** number is assigned from the
  `FWD/` sequence (no longer showing `/`). See `08-auto-open` for what happens next.
- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.

> **Note:** Approving a document whose Amount Unallocated is not zero is rejected with
> an error when the automatic Open transition runs -- see `08-auto-open`.
