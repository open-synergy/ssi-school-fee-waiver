# Edit Admission

> **Module:** `ssi_school_fee_waiver_admission`\
> **Extends:** ssi_school_admission — model `school_admission`, aksi `02-edit`

## Modified Validation

- **Compute Payment**, the **Copy Payment Term** wizard, and deleting a payment term row
  by hand will fail **if** a fee waiver refers to one of the payment terms being
  deleted. This covers a Single Payment Term waiver that points at the term, and a
  Multiple Payment Terms waiver that has a Schedule line pinned to the term. The waiver
  state does not matter.
- The error message names the payment term and the fee waiver that refers to it.
- A Multiple Payment Terms waiver that has no Schedule line yet (for example one still
  in **Draft**) does not block Compute Payment.
- To proceed, cancel the fee waiver first (see the fee waiver `10-cancel`), then
  recompute or delete the payment terms.
