// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_fee_waiver_admission.school_fee_waiver_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block, reused by every tour below -- Flow
    // step 1 of every IK in docs/school_fee_waiver/: "Open the
    // School > Fee Waiver > Fee Waivers menu." Duplicated from the
    // base module's own tour helper
    // (ssi_school_fee_waiver.school_fee_waiver_tour) since a JS
    // module registered by ``odoo.define`` does not export its
    // internal helpers to another module's file.
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

    // IK: docs/school_fee_waiver/01-create.md ("Additional Fields"
    // delta). Navigation (open menu -> New -> select Type/Reason/
    // Student) is the base IK's own Flow steps 1-3 -- see skill
    // odoo-development-ui-test, scope-and-boundaries.md §1 ("Backing
    // dua file: tour extension = base IK ∪ delta IK"). The delta
    // itself: switching Billing Source to Admission hides Enrollment
    // and reveals Admission; Payment Term is also hidden, so Coverage
    // is set to Multiple Payment Terms (Single Payment Term is not
    // wired for Admission by this module -- see the IK's own note).
    // The tour verifies the fields are present and the record is
    // saved, not the values it derives (that is
    // odoo-development-unit-test's job).
    tour.register(
        "ssi_school_fee_waiver_admission_school_fee_waiver_create",
        {test: true, url: "/web"},
        [].concat(openFeeWaiversList(), [
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
                content: "Select the Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                run: "text TOUR ADM FW Type",
            },
            {
                content: "Pick the Type from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item:not(.o_m2o_dropdown_option) a:contains(TOUR ADM FW Type)",
                in_modal: false,
            },
            {
                content: "Select the Reason",
                trigger: ".o_field_many2one[name='reason_id'] input",
                run: "text TOUR ADM FW Reason",
            },
            {
                content: "Pick the Reason from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item:not(.o_m2o_dropdown_option) a:contains(TOUR ADM FW Reason)",
                in_modal: false,
            },
            {
                content: "Select the Student",
                trigger: ".o_field_many2one[name='student_id'] input",
                run: "text TOUR ADM FW Student",
            },
            {
                content: "Pick the Student from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item:not(.o_m2o_dropdown_option) a:contains(TOUR ADM FW Student)",
                in_modal: false,
            },
            // ── Delta -- switch Billing Source to Admission, which
            // hides Enrollment/Payment Term and reveals Admission.
            {
                content: "Switch Billing Source to Admission",
                trigger: "select.o_field_widget[name='source_type']",
                run: "text Admission",
            },
            {
                content: "Admission field is now displayed",
                trigger: ".o_field_many2one[name='admission_id']",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Select the Admission",
                trigger: ".o_field_many2one[name='admission_id'] input",
                run: "text TOUR-ADM-FW-ADM-001",
            },
            {
                content: "Pick the Admission from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item:not(.o_m2o_dropdown_option) a:contains(TOUR-ADM-FW-ADM-001)",
                in_modal: false,
            },
            {
                content: "Switch Coverage to Multiple Payment Terms",
                trigger: "select.o_field_widget[name='coverage']",
                run: "text Multiple Payment Terms",
            },
            {
                content: "Fill in Start Date",
                trigger: ".o_field_widget[name='date_start'] input",
                run: "text 08/01/2026",
            },
            {
                content: "Fill in End Date",
                trigger: ".o_field_widget[name='date_end'] input",
                run: "text 10/31/2026",
            },
            // ── Base Flow -- add a Line so the record can be saved.
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
                run: "text TOUR ADM FW Product",
            },
            {
                content: "Pick the Product from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item:not(.o_m2o_dropdown_option) a:contains(TOUR ADM FW Product)",
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
        ])
    );

    // IK: docs/school_fee_waiver/07-generate-schedule.md ("Additional
    // Behavior" delta). Navigation and the button click are the base
    // IK's own Flow. The delta: the newly created Schedule line shows
    // the Admission Payment Term that was added after this waiver
    // already opened, not an Enrollment Payment Term.
    tour.register(
        "ssi_school_fee_waiver_admission_school_fee_waiver_generate_schedule",
        {test: true, url: "/web"},
        [].concat(openFeeWaiversList(), [
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR-ADM-FW-SCHEDULE-001) .o_data_cell:first",
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
            // ── Post-Condition -- a new Schedule line is created for
            // TOUR ADM FW SCHEDULE TERM B, the Admission Payment Term
            // added after this waiver already opened (and thus
            // already auto-generated its Schedule for Term A). Waiting
            // directly for this row -- rather than a generic "form
            // reloaded" signal -- is the only gate here guaranteed
            // false until the button's RPC actually finishes
            // (odoo-development-ui-test, patterns.md §P): Term B
            // cannot appear in any Schedule line before this button is
            // clicked.
            {
                content: "Open the Schedule tab",
                trigger: ".o_notebook .nav-link:contains(Schedule)",
            },
            {
                content: "A Schedule line for the new Admission Payment Term appears",
                trigger:
                    ".o_field_widget[name='schedule_ids'] .o_data_row:contains(TOUR ADM FW SCHEDULE TERM B)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );
});
