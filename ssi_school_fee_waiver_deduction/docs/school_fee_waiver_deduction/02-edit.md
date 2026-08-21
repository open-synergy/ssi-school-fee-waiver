# Edit Fee Waiver Deduction

> **Module:** ssi_school_fee_waiver_deduction\
> **Model:** `school_fee_waiver_deduction`\
> **Menu:** School > Fee Waiver > Fee Waiver Deductions\
> **Actor:** user in group `User`\
> **State:** `draft` (unchanged)\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Fee Waiver > Fee Waiver Deductions** menu.
2. Find and open the record to edit.
3. Change the required fields, the **Lines** tab, or the **Allocations** tab.
4. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- **Amount Total**, **Amount Allocated**, and **Amount Unallocated** are recomputed from
  the current Lines and Allocations.
