Glue module that lets a School Fee Waiver be billed against a
``school_admission`` instead of only a ``school_enrollment``. Adds
``admission`` as a second Billing Source value, and derives the
waiver's School/Grade/Academic Year/Partner and realization schedule
from the selected Admission's own payment terms once it has reached
state Open. Useful for waivers decided during admission, before the
student's enrollment record exists.
