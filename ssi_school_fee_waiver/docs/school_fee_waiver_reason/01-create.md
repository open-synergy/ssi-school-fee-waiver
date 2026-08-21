# Create Fee Waiver Reason

> **Module:** ssi_school_fee_waiver\
> **Model:** `school_fee_waiver_reason`\
> **Menu:** School > Configuration > Fee Waiver > Fee Waiver Reasons\
> **Actor:** user in group `Configurator`

## Pre-Condition

- **Access:** User is in group `Configurator`.

## Flow

1. Open the **School > Configuration > Fee Waiver > Fee Waiver Reasons** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the applicant-facing basis for the waiver request
     (e.g. "Economic Hardship", "Orphan", "Disaster", "Staff Family").
   - **Code** _(required)_: Enter a unique code identifying this fee waiver reason, or
     enter **/** to assign it later using **Generate Code**.
   - **Sequence**: Automatically defaulted to **10**. Change it to control the display
     order among Fee Waiver Reasons — lower values appear first.
4. Click **Save**.

## Post-Condition

- A new Fee Waiver Reason record is created and active.
- The new Fee Waiver Reason becomes selectable wherever a fee waiver reason is required.
