Glue module that lets a School Fee Waiver be billed against a
``school_admission`` instead of only a ``school_enrollment``. Adds
``admission`` as a second Billing Source value, and derives the
waiver's School/Grade/Academic Year/Partner and realization schedule
from the selected Admission's own payment terms once it has a School Student
profile (created with Create Student Profile, or when it reaches
state Open). Useful for waivers decided during admission, before the
student's enrollment record exists. While a fee waiver refers to an
Admission's payment terms, those terms cannot be deleted, and the
Admission cannot be cancelled while the waiver is active.
