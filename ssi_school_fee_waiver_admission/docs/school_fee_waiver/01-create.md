# Create Fee Waiver

> **Module:** ssi_school_fee_waiver_admission\
> **Extends:** ssi_school_fee_waiver -- model `school_fee_waiver`, action `01-create`

## Additional Fields

When this module is installed, **Billing Source** gains a second value:

- **Billing Source**: now also offers **Admission**, alongside the base module's
  **Enrollment**.
- **Admission** _(required when Billing Source is Admission)_: Select the admission this
  waiver is billed against, restricted to admissions already linked to the selected
  Student's School Student record -- an admission that has not yet reached **Open** has
  not created one yet, so it cannot be billed against. Hidden when Billing Source is not
  Admission. Selecting it fills Partner, School, Grade, and Academic Year, the same as
  Enrollment does.
- **Payment Term** is now also hidden when Billing Source is Admission. Building an
  Admission-sourced waiver's Schedule against a single term of the Admission is not yet
  supported by this module -- set Coverage to **Multiple Payment Terms** when Billing
  Source is Admission; see `07-generate-schedule`.
