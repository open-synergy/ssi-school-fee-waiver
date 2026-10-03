# Cancel Enrollment

> **Module:** `ssi_school_fee_waiver`\
> **Extends:** ssi_school — model `school_enrollment`, aksi `10-cancel`

## Modified Validation

- Cancelling an enrollment will fail **if** a fee waiver billed against that enrollment
  is still active, that is, its status is **Draft**, **Waiting for Approval**, **On
  Progress**, or **Done**.
- The error message names the active fee waiver.
- To proceed, cancel (or reject) the fee waiver first, then cancel the enrollment. A
  waiver that is already **Cancelled** or **Rejected** does not block cancellation.
