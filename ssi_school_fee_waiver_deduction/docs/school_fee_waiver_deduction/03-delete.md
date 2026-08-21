# Delete Fee Waiver Deduction

> **Module:** ssi_school_fee_waiver_deduction\
> **Model:** `school_fee_waiver_deduction`\
> **Menu:** School > Fee Waiver > Fee Waiver Deductions\
> **Actor:** user in group `User`\
> **State:** `draft` (removed)\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Fee Waiver > Fee Waiver Deductions** menu.
2. Select one or more Draft records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
