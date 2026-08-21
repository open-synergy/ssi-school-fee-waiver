odoo.define("ssi_school_fee_waiver.school_fee_waiver_type_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    function openMenuSteps() {
        return [
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
            // "Fee Waiver" (menu_school_fee_waiver_configuration) has children and is
            // level 3, so it is rendered as a non-clickable dropdown header without
            // data-menu-xmlid — skip straight to the Fee Waiver Types leaf item.
            {
                content: "Open the Fee Waiver Types menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_fee_waiver.school_fee_waiver_type_menu"]',
            },
            {
                content: "Fee Waiver Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Fee Waiver Types)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                    return true;
                },
            },
        ];
    }

    // IK: docs/school_fee_waiver_type/01-create.md
    tour.register(
        "ssi_school_fee_waiver_school_fee_waiver_type_create",
        {test: true, url: "/web"},
        [
            ...openMenuSteps(),
            {
                content: "Click Create",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only.
                    return true;
                },
            },
            {
                content: "Fill in Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Tour Fee Waiver Type New",
            },
            {
                content: "Fill in Code",
                trigger: ".o_field_widget[name='code']",
                run: "text TOUR-FWT-NEW",
            },
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only.
                    return true;
                },
            },
        ]
    );

    // IK: docs/school_fee_waiver_type/02-edit.md
    tour.register(
        "ssi_school_fee_waiver_school_fee_waiver_type_edit",
        {test: true, url: "/web"},
        [
            ...openMenuSteps(),
            {
                content: "Open the fee waiver type to edit",
                trigger: ".o_data_row:contains(Tour Fee Waiver Type Edit)",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Click Edit",
                trigger: ".o_form_button_edit",
            },
            {
                content: "Change the Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Tour Fee Waiver Type Edited",
            },
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only.
                    return true;
                },
            },
        ]
    );

    // IK: docs/school_fee_waiver_type/03-delete.md
    tour.register(
        "ssi_school_fee_waiver_school_fee_waiver_type_delete",
        {test: true, url: "/web"},
        [
            ...openMenuSteps(),
            {
                content: "Open the fee waiver type to delete",
                trigger: ".o_data_row:contains(Tour Fee Waiver Type Delete)",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Delete",
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Delete";
                        }
                    );
                    $delete[0].click();
                },
            },
            {
                content: "Confirm deletion",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Click the Fee Waiver Types breadcrumb to return to the list",
                trigger: ".breadcrumb-item.o_back_button a:contains(Fee Waiver Types)",
            },
            {
                content: "Back to the list",
                trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                    return true;
                },
            },
        ]
    );
});
