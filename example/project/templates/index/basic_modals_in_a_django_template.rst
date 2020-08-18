{% verbatim %}

Basic modals in a Django template
=================================

Objectives
----------

Moving our attention to a dynamic site based on Django, our main objectives become:

- having a dialog box, to be used as "container" for user interaction, whose layout
  is coherent with the front-end pages
- the content and life cycle of the dialog can be controlled "server-side"
- the dialog will close when the user has completed or cancelled the operation

Usage
-----

The solution provided by `django-frontend-forms` requires two actions:

1) to provide an HTML template for the dialog layout
2) attach the template to a `Dialog()` javascript object to control it's behaviour

Since in most cases you will be primarily interested in customizing the modal
content only, a default template is provided to render a generic dialog
(file `frontend_forms/templates/frontend_forms/dialogs.html`):

.. code:: html

    <div id="dialog_generic" class="dialog draggable">
        <div class="dialog-dialog">
            <div class="dialog-content">
                <div class="dialog-header">
                    <span class="spinner">
                        <i class="fa fa-spinner fa-spin"></i>
                    </span>
                    <span class="close">&times;</span>
                    <div class="title">Title</div>
                </div>
                <div class="dialog-body ui-front">
                    {% comment %}
                    <p>Some text in the dialog ...</p>
                    {% endcomment %}
                </div>
                <div class="dialog-footer">
                    <input type="submit" value="Close" class="btn btn-close" />
                    <input type="submit" value="Save" class="btn btn-save" />
                    <div class="text">footer</div>
                </div>
            </div>
        </div>
    </div>

When instantiating the javascript `Dialog` object, you can select an alternative
template instead, providing a suitable value for `djalog_selector`:

.. code:: javascript

    $(document).ready(function() {

        dialog1 = new Dialog({
            dialog_selector: '#dialog_generic',
            html: '<h1>Loading ...</h1>',
            width: '400px',
            min_height: '200px',
            title: '<i class="fa fa-calculator"></i> Select an object ...',
            footer_text: 'testing dialog ...'
        });

    });

It is advisable to use an HTML structure similar to the default layout;

Notes:

- adding ".ui-front" to the ".dialog-box" element helps improving the behaviour of the dialog on a mobile client
- adding class ".draggable" makes the Dialog draggable - this is optional, and requires jquery-ui

Opening a static Dialog
-----------------------

The layout of the Dialog is fully described by the referenced HTML template:
either the default "#dialog_generic" of a specific one.

You can fully customize the rendering with CSS; the default styles are provided
by `static/frontend_forms/css/frontend_forms.css`

.. code:: javascript

    dialog1 = new Dialog({
        dialog_selector: '#dialog_generic',
        html: '<h1>Static content goes here ...</h1>',
        width: '600px',
        min_height: '200px',
        title: '<i class="fa fa-calculator"></i> Select an object ...',
        footer_text: 'testing dialog ...',
        enable_trace: true
    });

    dialog1.open()

.. figure:: /static/images/static_dialog.png

   A simple static Dialog

Opening a dynamic Dialog
------------------------

In most cases, you will rather produce the dialog content dynamically.

To obtain that, just add an "url" option to the Djalog constructor,
and it will be automatically used to obtain the Dialog content from the server via an Ajax call.

.. code:: javascript

    dialog1 = new Dialog({
        ...
        url: "{% url 'samples:simple-content' %}",
        ...

Sometimes it is convenient to reuse the very same single view to render either a
modal dialog, or a standalone HTML page.

This can be easily accomplished providing:

- an "inner" template which renders the content
- an "outer" container template which renders the full page, then includes the "inner" template
- in the view, detect the call context and render one or another

.. code:: python

    def simple_content2(request):

        # Either render only the modal content, or a full standalone page
        if request.is_ajax():
            template_name = 'frontend/includes/simple_content2_inner.html'
        else:
            template_name = 'frontend/includes/simple_content2.html'

        return render(request, template_name, {
        })

here, the "inner" template provides the content:

.. code:: html

    <div class="row">
        <div class="col-sm-4">
            {% lorem 1 p random %}
        </div>
        <div class="col-sm-4">
            {% lorem 1 p random %}
        </div>
        <div class="col-sm-4">
            {% lorem 1 p random %}
        </div>
    </div>

while the "outer" one renders the full page:

.. code:: html

    {% extends "base.html" %}
    {% load static staticfiles i18n %}

    {% block content %}
    {% include 'frontend/includes/simple_content2_inner.html' %}
    {% endblock content %}

More examples are available here:

.. note::

    Code sample: |link_simple-dialogs|

.. |link_simple-dialogs| raw:: html

   <a href="/samples/simple-dialogs/" target="_blank">Simple Dialogs with Django</a>

Files organization
------------------

You should include the default styles and the javascript support in your base template.

For convenience, a sample HTML template has been provided for a generic dialog,
and should be included as well.

.. code:: html

    <link rel="stylesheet" href="{% static 'frontend_forms/css/frontend_forms.css' %}">
    <script src="{% static 'frontend_forms/js/frontend_forms.jsx' %}"></script>

    {% block modals %}
        {% include 'frontend_forms/dialogs.html' %}
    {% endblock modals %}


Since the js code uses the `class` keyword, you might want to transpile `frontend_forms.jsx`
with Babel for maximum compatibility, to support oldest browsers.


{% endverbatim %}
