# Auto-Open Fee Waiver

> **Module:** `ssi_school_fee_waiver`\
> **Model:** `school_fee_waiver`\
> **Menu:** School > Fee Waiver > Fee Waivers\
> **Actor:** System — triggered automatically, no user interaction\
> **State:** `confirm` → `open`\
> **Requires:** `05-approve`

There is no **Start** button on this model: the mixin-inserted button
(`attrs="{'invisible':[('open_ok','!=',True)]}"`) never becomes visible, since this
model's policy template has no active row for `open_ok`. The transition to **On
Progress** is performed automatically by `action_approve_approval` itself, right after
the last pending approval level is fulfilled.

## Pre-Condition

- **Record:** All approval levels for this waiver have just been fulfilled (the last
  step of `05-approve`).

## Flow

This transition has no click steps — it is triggered automatically by the system as part
of `05-approve`. A user (an approver on the pending level) clicks **Approve**; once
every approval level is fulfilled, the waiver moves straight to **On Progress** without
a separate action.

## Post-Condition

- Status changes to **On Progress**, shown on the statusbar.
- The waiver's Schedule is generated -- see `07-generate-schedule`.
