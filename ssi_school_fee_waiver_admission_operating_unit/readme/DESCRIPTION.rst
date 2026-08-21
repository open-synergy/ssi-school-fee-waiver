Glue module bridging ``ssi_school_fee_waiver_admission`` and
``ssi_school_fee_waiver_operating_unit``. A fee waiver billed against
an Admission gets its ``operating_unit_id`` derived from the
Admission's own school, using the same "exactly one operating unit"
contract as the existing Enrollment-sourced derivation. Adds no
field, no view, and no security rule of its own -- both are already
provided by the two modules it bridges.
