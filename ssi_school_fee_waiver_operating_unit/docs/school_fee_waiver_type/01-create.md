# Create Fee Waiver Type

> **Module:** ssi_school_fee_waiver_operating_unit\
> **Extends:** ssi_school_fee_waiver — model `school_fee_waiver_type`, action `01-create`

## Additional Fields

When this module is installed, the create form gains one optional field:

- **Operating Unit**: Select the operating unit this Fee Waiver Type belongs to. Leave
  empty to make the record visible to every operating unit. Only visible to users in the
  _Multiple Operating Unit_ group.

## Modified — Record Visibility

- The Fee Waiver Type list is filtered by a record rule: a user only sees records that
  have no Operating Unit set, or that share their own Operating Unit. This rule only
  restricts what a user can see — it does not restrict who can create, edit, or delete
  records.
