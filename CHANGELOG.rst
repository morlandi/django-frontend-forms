.. :changelog:

History
=======

v0.3.3
------
- css cleanup (to keep Whitenoise happy)

v0.3.2
------
- rewrite utilities for vanilla JS

v0.3.1
------
- accept JSON response after form validation

v0.3.0
------
- optionally replace "frontend_form.js" with "frontend_form_vanilla.js"
- upgrade to Django 4.2

v0.2.20
-------
- generic_edit_view() now treats request.FILES

v0.2.19
-------
- [fix] frontend_forms.js was out of sync with frontend_forms.jsx

v0.2.18
-------
- [fix] "it" language selection for datepicker
- formdata_serialize() and formdata_to_querystring() helpers added

v0.2.17
-------
* diplay_message() helper added

v0.2.16
-------
* small style fix for checkbox in horizontal generic form rendering

v0.2.15
-------
* revised example project

v0.2.14
-------
* Prepare for Django 4.0

v0.2.13
-------
* POSSIBLE INCOMPATIBLE CHANGE: Radio button layout refactored in "render_form_field.html"
* send "submission_failure" notification
* package up data from form with FormData (instead of form.serialize()) to allow files upload
* allow customization of `enctype` in generic form template
* send "submission_failure" notification

v0.2.12
-------
* Prevent default on close button submission

v0.2.11
-------
* Replace $() with jQuery() for higher compatibility

v0.2.10
-------
* Add never cache to all views for extra safeness

v0.2.9
------
* [fix] Properly hide btn_save and btn_close when corresponding label is empty

v0.2.8
------
* [fix] frontend_forms.js was out of sync with frontend_forms.jsx

v0.2.7
------
* Removed wrong [fix] render_form_field rendering for bootstrap

v0.2.6
------
* Update Pillow (example project)

v0.2.5
------
* Upgrade Django (in example project)
* [fix] render_form_field rendering for bootstrap
* Optionally retrieve missing Dialog options from HTML attributes
* subtitle added to dialog_generic

v0.2.4
------
* in case of form errors, autofocus now selects the first editable invalid field

v0.2.3
------
* transpile frontend_forms.jsx

v0.2.2
------
* non-destructive form_class annotation

v0.2.1
------
* POSSIBLE INCOMPATIBLE CHANGE: Added javascript catalog for translating messages in JS code
* Italian transation added
* Example: chain selection sample
* [fix] Send missing "submitted" notification

v0.2.0
------
* Login view suitable for modal forms
* check_logged_in() decorator
* fix format_datetime
* POSSIBLE INCOMPATIBLE CHANGE: provided templates now extend "base.html" instead of "frontend/base.html"

v0.1.13
-------
* Improved example project (Creating or updating a Django Model from the front-end)
* revised confirmRemoteAction() helper

v0.1.12
-------
* Make sure invalid-tooltip is visible with BS4

v0.1.11
-------
* Select2 support and examples

v0.1.10
-------
* Small adjustments to default styles; "important" removed where possible
* Partial support for Bootstrap's "input-group-addon"
* Example updated

v0.1.9
------
* Giving a feedback after successful form submission

v0.1.8
------
* Make sure Sweetalert2 pops up above modal dialog

v0.1.7
------
* render_form_field: show errors for radio groups

v0.1.6
------
* example django project added

v0.1.5
------
* autofocus_first_visible_input option added

v0.1.4
------
* generic Form submission from a Dialog example added to Readme
* fix horizontal forms for BS4
* add even/odd class to form groups

v0.1.3
------
* Display checkbox fields errors
* Adjust errors styles

v0.1.2
------
* Optionally provide the `request` to the Form constructor
* Add a class attribute 'form-app_label-model_name' to the rendered form
* django-select2 support
* jQuery MultiSelect support

v0.1.1
------
* ModalForms module renamed as FrontendForms
* optional parameter `event` added to open()

v0.1.0
------
* Module renamed from "django-modal-forms" to "django-frontend-forms"

v0.0.14
-------
* Fixes for Django 3; support both int and uuid PKs

v0.0.13
-------
* Configurable FRONTEND_FORMS_FORM_LAYOUT_DEFAULT

v0.0.12
-------
* Support for model forms in a Dialog (undocumented)

v0.0.11
-------
* Datepicker support

v0.0.10
-------
* optional extra_attrs added to render_form_field template tag

v0.0.9
------
* fix confirmRemoteAction()

v0.0.8
------
* fix

v0.0.7
------
* add custom widget attrs when rendering a field with render_form_fields()

v0.0.6
------
* add "has-error" class when appropriate in render_form_field tag, to trigger errors in modal forms

v0.0.5
------
* "simpletable" fix

v0.0.4
------
* "simpletable" styles

v0.0.3
------
* downloadFromAjaxPost helper JS function added
* Display non_field_errors in BS4 form
* Prepend fields' class with 'field-' prefix, as Django admin does
* Radio buttons and Checkboxs rendering for Bootstrap 4
* bs4 form rendering
* querystring_parse() utility added
* Add object_id hidden field to generic form
* .ui-front added to .dialog-body for bette behaviour on mobiles
* notify "loaded" event in _form_ajax_submit() when approriate

v0.0.2
------
* First working release

v0.0.1
------
* Project start
