odoo.define(
    "ssi_school_fee_waiver_deduction.school_fee_waiver_deduction_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Shared navigation block, reused verbatim by every tour below --
        // Flow step 1 of every IK in docs/school_fee_waiver_deduction/:
        // "Open the School > Fee Waiver > Fee Waiver Deductions menu."
        // Same 3-level shape (App root > Fee Waiver > leaf) already
        // proven clickable by ssi_school_fee_waiver's own
        // openFeeWaiversList() helper (odoo-development-ui-test,
        // patterns.md §A).
        function openFeeWaiverDeductionsList() {
            return [
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Fee Waiver menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_fee_waiver.menu_school_fee_waiver"]',
                },
                {
                    content: "Open the Fee Waiver Deductions menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_fee_waiver_deduction.school_fee_waiver_deduction_menu"]',
                },
                {
                    // Gate: wait for the Fee Waiver Deductions action to
                    // actually be mounted, not just any list view left
                    // over from the landing action (patterns.md §A).
                    content: "Fee Waiver Deductions list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Fee Waiver Deductions)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ];
        }

        function openRecord(searchText) {
            return [
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(" + searchText + ") .o_data_cell:first",
                },
                {
                    content: "Form is open",
                    trigger: ".o_form_view",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ];
        }

        function confirmDialog() {
            return [
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
            ];
        }

        // IK: docs/school_fee_waiver_deduction/01-create.md
        tour.register(
            "ssi_school_fee_waiver_deduction_create",
            {test: true, url: "/web"},
            [].concat(openFeeWaiverDeductionsList(), [
                {
                    content: "Click New",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
                {
                    content: "Select the Waiver",
                    trigger: ".o_field_many2one[name='waiver_id'] input",
                    run: "text TOUR-FWD-WAIVER-CREATE",
                },
                {
                    content: "Pick the Waiver from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-FWD-WAIVER-CREATE)",
                    in_modal: false,
                },
                {
                    content: "Journal was defaulted from the Waiver's own Type",
                    trigger: ".o_field_many2one[name='journal_id'] input",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
                {
                    content: "Select the Receivable Account",
                    trigger: ".o_field_many2one[name='receivable_account_id'] input",
                    run: "text TOUR FWD Receivable Account",
                },
                {
                    content: "Pick the Receivable Account from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR FWD Receivable Account)",
                    in_modal: false,
                },
                {
                    content: "Open the Lines tab",
                    trigger: ".o_notebook .nav-link:contains(Lines)",
                },
                {
                    content: "Add a Line",
                    trigger:
                        ".o_field_widget[name='line_ids'] .o_field_x2many_list_row_add a",
                },
                {
                    // Domain restricts this dropdown to the selected
                    // Waiver's own Schedule -- the dedicated Create
                    // waiver has exactly one, so the default (untyped)
                    // result list already has just one candidate.
                    content: "Open the Schedule dropdown",
                    trigger:
                        ".o_selected_row .o_field_widget[name='schedule_id'] input",
                    run: "click",
                },
                {
                    content: "Pick the only Schedule line",
                    trigger: ".ui-autocomplete .ui-menu-item:eq(0) a",
                    in_modal: false,
                },
                {
                    content: "Account was defaulted from the Schedule's own Type",
                    trigger: ".o_selected_row .o_field_widget[name='account_id']",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
                {
                    content: "Fill in the Amount",
                    trigger: ".o_selected_row input[name='amount']",
                    run: "text 1000000",
                },
                {
                    content: "Commit the Line",
                    trigger: ".o_field_widget[name='line_ids']",
                    run: "click",
                },
                {
                    content: "Open the Allocations tab",
                    trigger: ".o_notebook .nav-link:contains(Allocations)",
                },
                {
                    content: "Add an Allocation",
                    trigger:
                        ".o_field_widget[name='allocation_ids'] .o_field_x2many_list_row_add a",
                },
                {
                    // Domain restricts this dropdown to the Waiver's own
                    // Partner, open state, positive residual -- the
                    // dedicated Create invoice is the only match.
                    content: "Open the Customer Invoice dropdown",
                    trigger:
                        ".o_selected_row .o_field_widget[name='customer_invoice_id'] input",
                    run: "click",
                },
                {
                    content: "Pick the only Customer Invoice",
                    trigger: ".ui-autocomplete .ui-menu-item:eq(0) a",
                    in_modal: false,
                },
                {
                    content: "Fill in the Allocation Amount",
                    trigger: ".o_selected_row input[name='amount']",
                    run: "text 1000000",
                },
                {
                    content: "Commit the Allocation",
                    trigger: ".o_field_widget[name='allocation_ids']",
                    run: "click",
                },
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ])
        );

        // IK: docs/school_fee_waiver_deduction/04-confirm.md
        tour.register(
            "ssi_school_fee_waiver_deduction_confirm",
            {test: true, url: "/web"},
            [].concat(
                openFeeWaiverDeductionsList(),
                openRecord("TOUR FWD Student CONFIRM"),
                [
                    {
                        content: "Click the Confirm button",
                        trigger: ".o_statusbar_buttons button[name='action_confirm']",
                        extra_trigger: ".o_form_view",
                    },
                ],
                confirmDialog(),
                [
                    {
                        content: "Status is Waiting for Approval",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                        extra_trigger: "body:not(:has(.modal))",
                        run: function () {
                            // Assertion only; do not trigger the default click.
                        },
                    },
                ]
            )
        );

        // IK: docs/school_fee_waiver_deduction/05-approve.md
        tour.register(
            "ssi_school_fee_waiver_deduction_approve",
            {test: true, url: "/web"},
            [].concat(
                openFeeWaiverDeductionsList(),
                openRecord("TOUR FWD Student APPROVE"),
                [
                    {
                        content: "Click the Approve button",
                        trigger:
                            ".o_statusbar_buttons button[name='action_approve_approval']",
                        extra_trigger: ".o_form_view",
                    },
                ],
                confirmDialog(),
                [
                    {
                        // The fixture's single approval level is
                        // fulfilled by admin, the tour user, on this
                        // first Approve click -- auto-opens.
                        content: "Status is On Progress",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                        extra_trigger: "body:not(:has(.modal))",
                        run: function () {
                            // Assertion only; do not trigger the default click.
                        },
                    },
                ]
            )
        );

        // IK: docs/school_fee_waiver_deduction/06-reject.md
        tour.register(
            "ssi_school_fee_waiver_deduction_reject",
            {test: true, url: "/web"},
            [].concat(
                openFeeWaiverDeductionsList(),
                openRecord("TOUR FWD Student REJECT"),
                [
                    {
                        content: "Click the Reject button",
                        trigger:
                            ".o_statusbar_buttons button[name='action_reject_approval']",
                        extra_trigger: ".o_form_view",
                    },
                ],
                confirmDialog(),
                [
                    {
                        content: "Status is Rejected",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='reject'].btn-primary",
                        extra_trigger: "body:not(:has(.modal))",
                        run: function () {
                            // Assertion only; do not trigger the default click.
                        },
                    },
                ]
            )
        );

        // IK: docs/school_fee_waiver_deduction/09-finish.md
        tour.register(
            "ssi_school_fee_waiver_deduction_finish",
            {test: true, url: "/web"},
            [].concat(
                openFeeWaiverDeductionsList(),
                openRecord("TOUR FWD Student FINISH"),
                [
                    {
                        content: "Click the Done button",
                        trigger: ".o_statusbar_buttons button[name='action_done']",
                        extra_trigger: ".o_form_view",
                    },
                ],
                confirmDialog(),
                [
                    {
                        content: "Status is Done",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                        extra_trigger: "body:not(:has(.modal))",
                        run: function () {
                            // Assertion only; do not trigger the default click.
                        },
                    },
                ]
            )
        );

        // IK: docs/school_fee_waiver_deduction/10-cancel.md
        tour.register(
            "ssi_school_fee_waiver_deduction_cancel",
            {test: true, url: "/web"},
            [].concat(
                openFeeWaiverDeductionsList(),
                openRecord("TOUR FWD Student CANCEL"),
                [
                    // The Cancel button is a `type="action"` button, so
                    // its `name` attribute is a numeric action id in
                    // the DOM; target it by label instead
                    // (selectors.md §4).
                    {
                        content: "Click the Cancel button",
                        trigger:
                            ".o_statusbar_buttons button:enabled:contains('Cancel')",
                        extra_trigger: ".o_form_view",
                    },
                    {
                        // The wizard renders cancel_reason_id with
                        // widget="radio" -- select the matching radio
                        // item by its label text. 14.0: do NOT prefix
                        // the trigger with `.modal` (patterns.md §H).
                        content: "Select the Cancellation Reason",
                        trigger:
                            ".o_field_widget[name='cancel_reason_id'] .o_radio_item:contains(TOUR FWD Cancel Reason) input",
                        in_modal: true,
                    },
                    {
                        content: "Confirm the wizard",
                        trigger: ".modal-footer button[name='action_confirm']",
                    },
                ],
                confirmDialog(),
                [
                    {
                        content: "Status is Cancelled",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                        extra_trigger: "body:not(:has(.modal))",
                        run: function () {
                            // Assertion only; do not trigger the default click.
                        },
                    },
                ]
            )
        );

        // IK: docs/school_fee_waiver_deduction/12-restart.md
        tour.register(
            "ssi_school_fee_waiver_deduction_restart",
            {test: true, url: "/web"},
            [].concat(
                openFeeWaiverDeductionsList(),
                openRecord("TOUR FWD Student RESTART"),
                [
                    {
                        content: "Click the Restart button",
                        trigger: ".o_statusbar_buttons button[name='action_restart']",
                        extra_trigger: ".o_form_view",
                    },
                ],
                confirmDialog(),
                [
                    {
                        content: "Status is Draft",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                        extra_trigger: "body:not(:has(.modal))",
                        run: function () {
                            // Assertion only; do not trigger the default click.
                        },
                    },
                ]
            )
        );

        // IK: docs/school_fee_waiver_deduction/14-restart-approval.md
        tour.register(
            "ssi_school_fee_waiver_deduction_restart_approval",
            {test: true, url: "/web"},
            [].concat(
                openFeeWaiverDeductionsList(),
                openRecord("TOUR FWD Student RAPPROVAL"),
                [
                    {
                        content: "Click the Restart Approval Process button",
                        trigger:
                            ".o_statusbar_buttons button[name='action_reload_approval_template']",
                        extra_trigger: ".o_form_view",
                    },
                ],
                confirmDialog(),
                [
                    {
                        content: "Status is still Waiting for Approval",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                        extra_trigger: "body:not(:has(.modal))",
                        run: function () {
                            // Assertion only; do not trigger the default click.
                        },
                    },
                ]
            )
        );
    }
);
