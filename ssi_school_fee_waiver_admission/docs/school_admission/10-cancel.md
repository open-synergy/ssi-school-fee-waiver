# Cancel Admission

> **Module:** `ssi_school_fee_waiver_admission`\
> **Extends:** ssi_school_admission — model `school_admission`, aksi `10-cancel`

## Modified Validation

- Cancelling an admission will fail **if** a fee waiver billed against that admission is
  still active, that is, its status is **Draft**, **Waiting for Approval**, **On
  Progress**, or **Done**.
- The error message names the active fee waiver.
- To proceed, cancel (or reject) the fee waiver first, then cancel the admission. A
  waiver that is already **Cancelled** or **Rejected** does not block cancellation.
