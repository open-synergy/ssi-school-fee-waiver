odoo.define("ssi_school_fee_waiver.school_fee_waiver_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block, reused verbatim by every tour below --
    // Flow step 1 of every IK in docs/school_fee_waiver/: "Open the
    // School > Fee Waiver > Fee Waivers menu." "Fee Waiver"
    // (menu_school_fee_waiver) sits directly under the School app
    // root and has a single leaf child, so both levels are rendered
    // clickable in 14.0 (odoo-development-ui-test, patterns.md §A).
    function openFeeWaiversList() {
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
                content: "Open the Fee Waivers menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_fee_waiver.school_fee_waiver_menu"]',
            },
            {
                // Gate: wait for the Fee Waivers action to actually be
                // mounted, not just any list view left over from the
                // landing action (patterns.md §A).
                content: "Fee Waivers list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Fee Waivers)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ];
    }

    function fillHeaderFields(enrollmentName) {
        return [
            {
                content: "Select the Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                run: "text TOUR FW Type",
            },
            {
                content: "Pick the Type from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR FW Type)",
                in_modal: false,
            },
            {
                content: "Select the Reason",
                trigger: ".o_field_many2one[name='reason_id'] input",
                run: "text TOUR FW Reason",
            },
            {
                content: "Pick the Reason from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR FW Reason)",
                in_modal: false,
            },
            {
                content: "Select the Student",
                trigger: ".o_field_many2one[name='student_id'] input",
                run: "text TOUR FW Student",
            },
            {
                content: "Pick the Student from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR FW Student)",
                in_modal: false,
            },
            // Billing Source defaults to Enrollment and is left at
            // that default -- only its visibility is asserted here,
            // never its value (odoo-development-ui-test, tour tests
            // the click-flow, not compute/onchange results).
            {
                content: "Billing Source field is displayed",
                trigger: ".o_field_widget[name='source_type']",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Select the Enrollment",
                trigger: ".o_field_many2one[name='enrollment_id'] input",
                run: "text " + enrollmentName,
            },
            {
                content: "Pick the Enrollment from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(" + enrollmentName + ")",
                in_modal: false,
            },
        ];
    }

    function addLine() {
        return [
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
                content: "Select the Product",
                trigger: ".o_selected_row .o_field_widget[name='product_id'] input",
                run: "text TOUR FW Product",
            },
            {
                content: "Pick the Product from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR FW Product)",
                in_modal: false,
            },
            {
                // Plain Float fields in a 14.0 editable list render as
                // a bare <input> -- the selector must target the
                // input directly, not an .o_field_widget[name=...]
                // descendant.
                content: "Fill in the Percentage",
                trigger: ".o_selected_row input[name='percentage']",
                run: "text 50",
            },
            {
                content: "Commit the Line",
                trigger: ".o_selected_row .o_field_widget[name='product_id']",
                run: "click",
            },
        ];
    }

    // IK: docs/school_fee_waiver/01-create.md
    tour.register(
        "ssi_school_fee_waiver_school_fee_waiver_create",
        {test: true, url: "/web"},
        [].concat(
            openFeeWaiversList(),
            // ── Variant 1 — Coverage: Single Payment Term (default).
            [
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
            ],
            fillHeaderFields("TOUR-FW-ENR-001"),
            [
                {
                    content: "Coverage defaults to Single Payment Term",
                    trigger: "select.o_field_widget[name='coverage']",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
                {
                    content: "Select the Payment Term",
                    trigger: ".o_field_many2one[name='payment_term_id'] input",
                    run: "text TOUR-FW-TERM-001",
                },
                {
                    content: "Pick the Payment Term from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-FW-TERM-001)",
                    in_modal: false,
                },
            ],
            addLine(),
            [
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
            ],
            // ── Variant 2 — Coverage: Multiple Payment Terms.
            [
                {
                    content: "Back to the Fee Waivers list",
                    trigger: ".breadcrumb-item.o_back_button a:contains(Fee Waivers)",
                },
                {
                    content: "Back on the list",
                    trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
                {
                    content: "Click New again",
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
            ],
            fillHeaderFields("TOUR-FW-ENR-001"),
            [
                {
                    content: "Switch Coverage to Multiple Payment Terms",
                    trigger: "select.o_field_widget[name='coverage']",
                    run: "text Multiple Payment Terms",
                },
                {
                    content: "Payment Term is now hidden",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
                {
                    content: "Fill in the Start Date",
                    trigger: ".o_field_widget[name='date_start'] input",
                    run: "text 08/01/2026",
                },
                {
                    content: "Fill in the End Date",
                    trigger: ".o_field_widget[name='date_end'] input",
                    run: "text 09/30/2026",
                },
            ],
            addLine(),
            [
                {
                    content: "Save the second record",
                    trigger: ".o_form_button_save",
                },
                {
                    content: "Second record is saved",
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
            ]
        )
    );

    // IK: docs/school_fee_waiver/04-confirm.md
    tour.register(
        "ssi_school_fee_waiver_school_fee_waiver_confirm",
        {test: true, url: "/web"},
        [].concat(openFeeWaiversList(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-FW-CONFIRM-001) .o_data_cell:first",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Click the Confirm button",
                trigger: ".o_statusbar_buttons button[name='action_confirm']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Status is Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/school_fee_waiver/05-approve.md
    tour.register(
        "ssi_school_fee_waiver_school_fee_waiver_approve",
        {test: true, url: "/web"},
        [].concat(openFeeWaiversList(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-FW-APPROVE-001) .o_data_cell:first",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                // The fixture's single approval level is fulfilled by
                // admin, the tour user, on this first Approve click.
                content: "Status is On Progress",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/school_fee_waiver/06-reject.md
    tour.register(
        "ssi_school_fee_waiver_school_fee_waiver_reject",
        {test: true, url: "/web"},
        [].concat(openFeeWaiversList(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-FW-REJECT-001) .o_data_cell:first",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Click the Reject button",
                trigger: ".o_statusbar_buttons button[name='action_reject_approval']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Status is Rejected",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='reject'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/school_fee_waiver/07-generate-schedule.md
    tour.register(
        "ssi_school_fee_waiver_school_fee_waiver_generate_schedule",
        {test: true, url: "/web"},
        [].concat(openFeeWaiversList(), [
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR-FW-SCHEDULE-001) .o_data_cell:first",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Click the Generate Schedule button",
                trigger: ".o_statusbar_buttons button[name='action_generate_schedule']",
                extra_trigger: ".o_form_view",
            },
            // ── Post-Condition — a new Schedule line is created for
            // TOUR FW SCHEDULE TERM B, the Payment Term added after
            // this waiver already opened (and thus already
            // auto-generated its Schedule for the original term).
            // Waiting directly for this row -- rather than a generic
            // "form reloaded" signal -- is the only gate here
            // guaranteed false until the button's RPC actually
            // finishes (patterns.md §P): Term B cannot appear in any
            // Schedule line before this button is clicked.
            {
                content: "Open the Schedule tab",
                trigger: ".o_notebook .nav-link:contains(Schedule)",
            },
            {
                content: "A Schedule line for the new Payment Term appears",
                trigger:
                    ".o_field_widget[name='schedule_ids'] .o_data_row:contains(TOUR FW SCHEDULE TERM B)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/school_fee_waiver/09-finish.md
    tour.register(
        "ssi_school_fee_waiver_school_fee_waiver_finish",
        {test: true, url: "/web"},
        [].concat(openFeeWaiversList(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-FW-FINISH-001) .o_data_cell:first",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Click the Done button",
                trigger: ".o_statusbar_buttons button[name='action_done']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Status is Done",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/school_fee_waiver/10-cancel.md
    tour.register(
        "ssi_school_fee_waiver_school_fee_waiver_cancel",
        {test: true, url: "/web"},
        [].concat(openFeeWaiversList(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-FW-CANCEL-001) .o_data_cell:first",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            // The Cancel button is a `type="action"` button, so its
            // `name` attribute is a numeric action id in the DOM;
            // target it by label instead (selectors.md §4).
            {
                content: "Click the Cancel button",
                trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                extra_trigger: ".o_form_view",
            },
            {
                // The wizard renders cancel_reason_id with
                // widget="radio" -- select the matching radio item by
                // its label text. 14.0: do NOT prefix the trigger
                // with `.modal` (patterns.md §H).
                content: "Select the Cancellation Reason",
                trigger:
                    ".o_field_widget[name='cancel_reason_id'] .o_radio_item:contains(TOUR FW Cancel Reason) input",
                in_modal: true,
            },
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },
            {
                // The wizard's own Confirm button carries
                // confirm="Are you sure?", stacking a second modal on
                // top of the wizard; 14.0 scopes the trigger search
                // to the topmost visible modal.
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Status is Cancelled",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/school_fee_waiver/12-restart.md
    tour.register(
        "ssi_school_fee_waiver_school_fee_waiver_restart",
        {test: true, url: "/web"},
        [].concat(openFeeWaiversList(), [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-FW-RESTART-001) .o_data_cell:first",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Click the Restart button",
                trigger: ".o_statusbar_buttons button[name='action_restart']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/school_fee_waiver/14-restart-approval.md
    tour.register(
        "ssi_school_fee_waiver_school_fee_waiver_restart_approval",
        {test: true, url: "/web"},
        [].concat(openFeeWaiversList(), [
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR-FW-RESTARTAPPR-001) .o_data_cell:first",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Click the Restart Approval Process button",
                trigger:
                    ".o_statusbar_buttons button[name='action_reload_approval_template']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Status is still Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );
});
