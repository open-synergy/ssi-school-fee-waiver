# Confirm Fee Waiver

> **Module:** ssi_school_fee_waiver\
> **Model:** `school_fee_waiver`\
> **Menu:** School > Fee Waiver > Fee Waivers\
> **Actor:** user in group `User`\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** At least one Line exists.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Fee Waiver > Fee Waivers** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**, shown on the statusbar.
- Approval records are created for each approver level defined by the approval template.

> **Note:** Confirming a waiver with no Line is rejected with an error -- see
> Pre-Condition above.
