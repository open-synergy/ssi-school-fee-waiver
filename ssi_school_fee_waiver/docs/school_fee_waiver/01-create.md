# Create Fee Waiver

> **Module:** ssi_school_fee_waiver\
> **Model:** `school_fee_waiver`\
> **Menu:** School > Fee Waiver > Fee Waivers\
> **Actor:** user in group `User`\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A `school_enrollment` exists for the target student, with at least one
  `school_enrollment_payment_term` (and its detail lines) already registered -- without
  it there is no billed amount for the Schedule to be based on.
- **Data:** A `school_fee_waiver_type` and a `school_fee_waiver_reason` exist.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Fee Waiver > Fee Waivers** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Type** _(required)_: Select the fee waiver type.
   - **Reason** _(required)_: Select the reason this waiver is being requested.
   - **Student** _(required)_: Select the student this waiver is granted to.
   - **Billing Source** _(required)_: Defaults to **Enrollment**, the only value this
     module registers.
   - **Enrollment** _(required when Billing Source is Enrollment)_: Select the
     enrollment this waiver is billed against, restricted to enrollments of the selected
     Student. Selecting it fills Partner, School, Grade, and Academic Year.
   - **Coverage** _(required)_: This is the field that distinguishes how the waiver
     repeats:
     - **Single Payment Term** _(default)_: fill in **Payment Term** _(required)_,
       restricted to payment terms of the selected Enrollment. The waiver closes out
       exactly that one term.
     - **Multiple Payment Terms**: **Payment Term** is hidden; instead fill in **Start
       Date** and **End Date** to bound the range of payment terms covered. Leaving
       either date empty means no bound on that side.
   - **Date**: Defaults to today's date.
4. On the **Lines** tab, add **at least one** line _(required before this waiver can be
   confirmed -- see `04-confirm`)_:
   - **Product** or **Product Category** _(exactly one required)_: Select the billing
     component this line covers -- a single Product, or a whole Product Category.
   - **Computation**: Defaults to **Percentage**. Change to **Fixed Amount** or **Full
     Coverage** if the waiver is not a percentage of the billed amount.
   - **Percentage** _(required, > 0 and up to 100, when Computation is Percentage)_.
   - **Fixed Amount** _(required, above zero, when Computation is Fixed Amount)_.
   - **Max Amount**: Leave at **0** for no ceiling.
5. Optionally fill in **Note** on the **Note** tab.
6. Click **Save**.

## Post-Condition

- A new Fee Waiver record is created in **Draft** status.
- **Amount Waived** stays zero: it is derived from the Schedule, which does not exist
  until this waiver reaches **On Progress** -- see `05-approve` and
  `07-generate-schedule`.
