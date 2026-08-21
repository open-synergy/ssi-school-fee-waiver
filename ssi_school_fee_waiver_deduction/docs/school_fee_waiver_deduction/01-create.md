# Create Fee Waiver Deduction

> **Module:** ssi_school_fee_waiver_deduction\
> **Model:** `school_fee_waiver_deduction`\
> **Menu:** School > Fee Waiver > Fee Waiver Deductions\
> **Actor:** user in group `User`\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `school_fee_waiver` exists in status **On Progress** or **Done**, with at
  least one Schedule line still **Scheduled** (not yet Realized, Skipped, or Cancelled).
- **Data:** At least one open `customer_invoice` exists for the waiver's own Partner,
  with a positive residual amount, to allocate against.
- **Data:** The waiver's own `school_fee_waiver_type` has Deduction Journal and Discount
  Account configured, so the Journal and Line Account default automatically.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Fee Waiver > Fee Waiver Deductions** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Waiver** _(required)_: Select the fee waiver document this deduction realizes.
     Selecting it fills Student and Partner, and defaults **Journal** from the waiver's
     own Fee Waiver Type.
   - **Journal** _(required)_: Defaults from the Waiver's Type; may be overridden.
   - **Receivable Account** _(required)_: Select the receivable account credited for the
     total deduction amount.
   - **Date**: Defaults to today's date.
4. On the **Lines** tab, add **at least one** line:
   - **Schedule** _(required)_: Select a Scheduled line of the selected Waiver.
     Selecting it defaults **Account** from the Schedule's own Waiver Type.
   - **Account** _(required)_: Defaults from the Schedule's own Waiver Type; may be
     overridden.
   - **Analytic Account**: Optional.
   - **Amount** _(required)_: The portion of the Schedule line's own Amount Planned
     being deducted now. May not exceed the Schedule line's remaining planned amount.
5. On the **Allocations** tab, add **at least one** line:
   - **Customer Invoice** _(required)_: Select an open invoice of the Waiver's own
     Partner with a positive residual.
   - **Amount** _(required)_: The portion of this document's Amount Total applied to the
     selected invoice. May not exceed the invoice's own residual.
6. Click **Save**.

## Post-Condition

- A new Fee Waiver Deduction record is created in **Draft** status.
- **Amount Total** is the sum of the Lines' own Amount; **Amount Allocated** is the sum
  of the Allocations' own Amount; **Amount Unallocated** is their difference, and must
  reach zero before this document can be opened -- see `04-confirm` and `08-auto-open`.
