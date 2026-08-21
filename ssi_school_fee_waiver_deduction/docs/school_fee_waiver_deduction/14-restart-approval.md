# Restart Fee Waiver Deduction Approval Process

> **Module:** ssi_school_fee_waiver_deduction\
> **Model:** `school_fee_waiver_deduction`\
> **Menu:** School > Fee Waiver > Fee Waiver Deductions\
> **Actor:** user in group `Validator`\
> **State:** `confirm` (unchanged)\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `restart_approval_ok` for state
  `confirm` to the actor's group.
- **Access:** User is in group `Validator`.

## Flow

1. Open the **School > Fee Waiver > Fee Waiver Deductions** menu.
2. Open the record whose approval process needs restarting.
3. Click the **Restart Approval Process** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status stays **Waiting for Approval**.
- The existing approval records are discarded and new ones are created from the approval
  template, starting again from the first approver level.
