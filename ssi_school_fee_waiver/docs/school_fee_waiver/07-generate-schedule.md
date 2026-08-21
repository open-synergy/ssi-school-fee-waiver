# Generate Fee Waiver Schedule

> **Module:** ssi_school_fee_waiver\
> **Model:** `school_fee_waiver`\
> **Menu:** School > Fee Waiver > Fee Waivers\
> **Actor:** user in group `User`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Config:** An active `policy.template` for this model grants `generate_schedule_ok`
  for state `open` to the actor's group.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Fee Waiver > Fee Waivers** menu.
2. Open an On Progress waiver.
3. Click the **Generate Schedule** button (`action_generate_schedule`).

## Post-Condition

- Every Schedule line still **Draft** or **Scheduled** is deleted, then one fresh line
  is (re)created on the **Schedule** tab per Line/Payment Term pairing eligible under
  the waiver's Coverage. A pairing that already has a Schedule line **Realized**,
  **Skipped**, or **Cancelled** is left untouched -- neither deleted nor duplicated.

> **Note:** A Schedule is also generated automatically, for every pairing eligible at
> that moment, the instant the waiver reaches **On Progress** -- see `05-approve`. This
> button exists so the schedule can be regenerated afterwards, e.g. once a Line changes
> or a new Payment Term becomes eligible under Multiple Payment Terms.
