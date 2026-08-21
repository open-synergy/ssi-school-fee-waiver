.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================
School Fee Waiver Deduction
=============================

Turns a fee waiver's plan into an accounting fact. Opening a Fee Waiver
Deduction document books its own journal entry -- crediting the student's
Receivable Account on the header, debiting a discount/contra-revenue account
per Deduction Line -- then reconciles that credit against one or more open
Customer Invoices, so their own residual amount drops and they move to Paid
once fully covered. Every realized Schedule line of the linked waiver moves
to Realized at the same time; cancelling the document reverses the
reconciliation, the journal entry, and every Schedule line it realized, all
at once or not at all.


Work Instruction
================

Fee Waiver Deduction
---------------------

* `Create Fee Waiver Deduction <docs/school_fee_waiver_deduction/01-create.html>`_
* `Edit Fee Waiver Deduction <docs/school_fee_waiver_deduction/02-edit.html>`_
* `Delete Fee Waiver Deduction <docs/school_fee_waiver_deduction/03-delete.html>`_
* `Confirm Fee Waiver Deduction <docs/school_fee_waiver_deduction/04-confirm.html>`_
* `Approve Fee Waiver Deduction <docs/school_fee_waiver_deduction/05-approve.html>`_
* `Reject Fee Waiver Deduction <docs/school_fee_waiver_deduction/06-reject.html>`_
* `Auto-Open Fee Waiver Deduction <docs/school_fee_waiver_deduction/08-auto-open.html>`_
* `Finish Fee Waiver Deduction <docs/school_fee_waiver_deduction/09-finish.html>`_
* `Cancel Fee Waiver Deduction <docs/school_fee_waiver_deduction/10-cancel.html>`_
* `Restart Fee Waiver Deduction <docs/school_fee_waiver_deduction/12-restart.html>`_
* `Restart Fee Waiver Deduction Approval Process <docs/school_fee_waiver_deduction/14-restart-approval.html>`_


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-school-fee-waiver
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *School Fee Waiver Deduction*
6.  Install the module


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/ssi-school-fee-waiver/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Andhitia Rama <andhitia.r@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
