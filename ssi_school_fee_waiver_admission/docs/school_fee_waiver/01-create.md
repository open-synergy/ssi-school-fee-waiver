# Create Fee Waiver

> **Module:** `ssi_school_fee_waiver_admission`\
> **Extends:** ssi_school_fee_waiver -- model `school_fee_waiver`, action `01-create`

## Additional Fields

When this module is installed, **Billing Source** gains a second value:

- **Billing Source**: now also offers **Admission**, alongside the base module's
  **Enrollment**.
- **Admission** _(required when Billing Source is Admission)_: Select the admission this
  waiver is billed against, restricted to non-cancelled, non-rejected admissions already
  linked to the selected Student's School Student record. An admission gets that record
  when you click **Create Student Profile** on it (while it is **Draft** or **Waiting
  for Approval**) or when it reaches **Open**; an admission without one cannot be billed
  against. Hidden when Billing Source is not Admission. Selecting it fills Partner,
  School, Grade, and Academic Year, the same as Enrollment does.
- **Payment Term** is now also hidden when Billing Source is Admission -- it names an
  Enrollment payment term, which does not apply to an Admission-sourced waiver.
- **Admission Payment Term** _(required when Billing Source is Admission and Coverage is
  Single Payment Term)_: Select the payment term of the selected Admission this waiver
  closes out, restricted to payment terms of that Admission. Hidden unless Billing
  Source is Admission and Coverage is Single Payment Term; must be left empty when
  Coverage is Multiple Payment Terms. Coverage Multiple Payment Terms still repeats the
  waiver over every payment term of the Admission that falls within Start Date/End Date,
  as described in `07-generate-schedule`.
