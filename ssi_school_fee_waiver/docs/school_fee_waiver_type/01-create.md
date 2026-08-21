# Create Fee Waiver Type

> **Module:** ssi_school_fee_waiver\
> **Model:** `school_fee_waiver_type`\
> **Menu:** School > Configuration > Fee Waiver > Fee Waiver Types\
> **Actor:** user in group `Configurator`

## Pre-Condition

- **Access:** User is in group `Configurator`.

## Flow

1. Open the **School > Configuration > Fee Waiver > Fee Waiver Types** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the fee waiver type (e.g. "Discretionary
     Waiver", "Scholarship-Linked Waiver").
   - **Code** _(required)_: Enter a unique code identifying this fee waiver type, or
     enter **/** to assign it later using **Generate Code**.
   - **Sequence**: Automatically defaulted to **10**. Change it to control the display
     order among Fee Waiver Types — lower values appear first.
4. Click **Save**.

## Post-Condition

- A new Fee Waiver Type record is created and active.
- The new Fee Waiver Type becomes selectable wherever a fee waiver type is required.
