# Finish Fee Waiver Deduction

> **Module:** ssi_school_fee_waiver_deduction\
> **Model:** `school_fee_waiver_deduction`\
> **Menu:** School > Fee Waiver > Fee Waiver Deductions\
> **Actor:** user in group `User`\
> **State:** `open` → `done`\
> **Requires:** `08-auto-open`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Config:** An active `policy.template` grants `done_ok` for state `open` to the
  actor's group.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Fee Waiver > Fee Waiver Deductions** menu.
2. Open the record to finish.
3. Click the **Done** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**, shown on the statusbar.
