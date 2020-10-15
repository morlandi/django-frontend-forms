.. :changelog:

History
=======

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
