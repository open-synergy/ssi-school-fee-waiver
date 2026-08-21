// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_school_fee_waiver_operating_unit.school_fee_waiver_type_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_fee_waiver_type/01-create.md (E1 delta --
        // Additional Fields). Navigation (open menu -> New) is taken
        // from the base IK ssi_school_fee_waiver/docs/
        // school_fee_waiver_type/01-create.md Flow steps 1-2 -- see
        // skill odoo-development-ui-test, scope-and-boundaries.md §1
        // ("Backing dua file: tour extension = base IK ∪ delta IK").
        // The delta assertion comes from this module's own IK: the
        // Operating Unit field is visible on the create form for a
        // user in the operating_unit.group_multi_operating_unit
        // group. The tour stops there; it does not fill, save, or
        // confirm (E1 delta-only).
        tour.register(
            "ssi_school_fee_waiver_operating_unit_school_fee_waiver_type_create",
            {
                test: true,
                url: "/web",
            },
            [
                // ── Base Flow 1 — Open the School > Configuration >
                // Fee Waiver > Fee Waiver Types menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Configuration menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_configuration"]',
                },
                // "Fee Waiver" (menu_school_fee_waiver_configuration) has
                // children and is level 3, so it is rendered as a
                // non-clickable dropdown header without data-menu-xmlid --
                // skip straight to the Fee Waiver Types leaf item.
                {
                    content: "Open the Fee Waiver Types menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_fee_waiver.school_fee_waiver_type_menu"]',
                },
                {
                    // Gate: wait for the TARGET action to be mounted, not
                    // just any list view (patterns.md §A).
                    content: "Fee Waiver Types list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Fee Waiver Types)",
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

                // ── Delta assertion — the Operating Unit field is
                // visible on the create form for a user in the multi
                // operating unit group. The tour stops here (E1
                // delta-only).
                {
                    content: "Operating Unit field is visible on the form",
                    trigger:
                        ".o_form_view.o_form_editable .o_field_widget[name='operating_unit_id']",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ]
        );
    }
);
