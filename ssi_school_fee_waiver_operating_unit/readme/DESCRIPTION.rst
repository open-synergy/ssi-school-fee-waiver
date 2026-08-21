Glue module that adds Operating Unit support to the School Fee Waiver
module. Extends ``school_fee_waiver``, ``school_fee_waiver_type``, and
``school_fee_waiver_reason`` with ``mixin.single_operating_unit``. The
fee waiver document's ``operating_unit_id`` is automatically derived
from the school of its selected Enrollment whenever that school
belongs to exactly one Operating Unit. Adds the matching security
group and record rules for all three models.
