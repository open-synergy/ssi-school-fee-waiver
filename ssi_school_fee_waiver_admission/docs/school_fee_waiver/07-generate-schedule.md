# Generate Fee Waiver Schedule

> **Module:** ssi_school_fee_waiver_admission\
> **Extends:** ssi_school_fee_waiver -- model `school_fee_waiver`, action `07-generate-schedule`

## Additional Post-Condition

When this waiver's Billing Source is **Admission**, the Schedule lines (re)created by
this button are built against the Admission's own payment terms instead of an
Enrollment's -- the Flow itself (click the same **Generate Schedule** button) is
unchanged:

- Each Schedule line's **Payment Term** field stays empty; **Admission Payment Term** is
  filled instead, pointing at a payment term of the selected Admission.
- Coverage **Multiple Payment Terms** repeats the waiver over every payment term of the
  Admission that falls within Start Date/End Date, exactly as it does against an
  Enrollment.
