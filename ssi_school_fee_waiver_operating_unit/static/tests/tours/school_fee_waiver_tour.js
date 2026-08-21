// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_fee_waiver_operating_unit.school_fee_waiver_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/school_fee_waiver/01-create.md ("Additional
    // Post-Condition" delta -- Operating Unit is derived, not
    // user-filled, mirroring ssi_school_operating_unit's
    // school_enrollment delta). Navigation (open menu -> New ->
    // select Type/Reason/Student/Enrollment) is taken from the
    // base IK ssi_school_fee_waiver/docs/school_fee_waiver/
    // 01-create.md Flow steps 1-3 -- see skill
    // odoo-development-ui-test, scope-and-boundaries.md §1
    // ("Backing dua file: tour extension = base IK ∪ delta IK").
    // The delta assertion comes from this module's own IK:
    // selecting the Enrollment (which also fills the related,
    // read-only school_id) auto-fills the Operating Unit field,
    // visible here as the m2o "open record" external button
    // appearing -- not the field's exact value, which is
    // odoo-development-unit-test's job. The tour stops there; it
    // does not fill Coverage/Payment Term or save.
    tour.register(
        "ssi_school_fee_waiver_operating_unit_school_fee_waiver_create",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Base Flow 1 — Open the School > Fee Waiver > Fee
            // Waivers menu.
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
                // Gate: wait for the TARGET action to be mounted, not
                // just any list view (patterns.md §A).
                content: "Fee Waivers list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Fee Waivers)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // ── Base Flow 2 — Click the New button. (14.0: "Create")
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

            // ── Base Flow 3 (partial) — Select Type, Reason,
            // Student, and Enrollment. Selecting the Enrollment is
            // what triggers this module's derivation (its
            // school_id ripples into this record's related,
            // read-only school_id, which this module's onchange
            // watches).
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
                run: "text TOUR OU FW Student",
            },
            {
                content: "Pick the Student from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR OU FW Student)",
                in_modal: false,
            },
            {
                content: "Select the Enrollment",
                trigger: ".o_field_many2one[name='enrollment_id'] input",
                run: "text TOUR-OU-FW-ENR-001",
            },
            {
                content: "Pick the Enrollment from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR-OU-FW-ENR-001)",
                in_modal: false,
            },

            // ── Delta assertion — the Operating Unit field is
            // auto-filled by the onchange this module registers on
            // school_id (which itself follows enrollment_id). The
            // "open record" external button on a many2one only
            // renders once the field carries a value, so its
            // presence is proof of "filled" without asserting which
            // operating unit it holds (odoo-development-ui-test,
            // scope-and-boundaries.md §2 -- exact value belongs to
            // odoo-development-unit-test).
            {
                content: "Operating Unit is auto-filled by the onchange",
                trigger:
                    ".o_field_many2one[name='operating_unit_id'] .o_external_button",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ]
    );
});
