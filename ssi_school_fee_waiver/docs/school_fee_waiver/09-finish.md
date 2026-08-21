# Finish Fee Waiver

> **Module:** ssi_school_fee_waiver\
> **Model:** `school_fee_waiver`\
> **Menu:** School > Fee Waiver > Fee Waivers\
> **Actor:** user in group `User`\
> **State:** `open` → `done`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Config:** An active `policy.template` grants `done_ok` for state `open` to the
  actor's group.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Fee Waiver > Fee Waivers** menu.
2. Open the record to finish.
3. Click the **Done** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**, shown on the statusbar.
