Form submission from a modal
============================

We've successfully injected data retrieved from the server in our modals,
but did not really interact with the user yet.

When the modal body contains a form, things start to become interesting and tricky.

Handling form submission
------------------------

When a form submission is involved, the modal life cycle has to be modified as follows:

- First and foremost, we need to **prevent the form from performing its default submit**.

  If not, after submission we'll be redirected to the form action, outside the context
  of the dialog.

  We'll do this binding to the form's submit event, where we'll serialize the form's
  content and sent it to the view for validation via an Ajax call.

- Then, upon a successufull response from the server, **we'll need to further investigate
  the HTML received**:

    + if it contains any field error, the form did not validate successfully,
      so we update the modal body with the new form and its errors

    + otherwise, user interaction is completed, and we can finally close the modal

`django-frontend-forms`, upon detecting a form in the content downloaded from the server,
already takes care of all these needs automatically, and keeps refreshing the modal
after each submission until the form validation succeedes.

.. figure:: /static/images/form_validation_1.png
   :scale: 80 %

   A form in the modal dialog

.. figure:: /static/images/form_validation_2.png
   :scale: 80 %

   While the form does not validate, we keep the dialog open

Implementation
--------------

If you're curious, here below is a detailed explanation of how all this is achieved.

Form detection happens at the end of modal opening:

.. code:: javascript

    open(event=null, show=true) {

        ...

        // Load remote content
        if (self.options.url) {
            self._load().done(function(data, textStatus, jqXHR) {
                var form = self.element.find('.dialog-content .dialog-body form');
                if (form.length == 1) {
                    // Manage form
                    self._form_ajax_submit();
                }
            });
        }
    }

In case, the code triggers a call to the helper method `_form_ajax_submit()`,
which is the real workhorse.

I developed it adapting the inspiring ideas presented in this brilliant article:

`Use Django's Class-Based Views with Bootstrap Modals <https://dmorgan.info/posts/django-views-bootstrap-modals/>`_

Here's the full code:

.. code:: javascript

    _form_ajax_submit() {
        var self = this;

        var content = self.element.find('.dialog-content');
        var header = content.find('.dialog-header');
        var body = content.find('.dialog-body');
        var footer = content.find('.dialog-footer');
        var form = content.find('.dialog-body form');

        // use footer save button, if available
        var btn_save = footer.find('.btn-save');
        if (btn_save) {
            form.find('.form-submit-row').hide();
            btn_save.off().on('click', function(event) {
                form.submit();
            });
        }

        // Give focus to first visible form field
        if (self.options.autofocus_first_visible_input) {
            form.find('input:visible').first().focus().select();
        }

        // bind to the form’s submit event
        form.on('submit', function(event) {

            // prevent the form from performing its default submit action
            event.preventDefault();
            header.addClass('loading');

            // serialize the form’s content and send via an AJAX call
            // using the form’s defined method and action
            var url = form.attr('action') || self.options.url;
            var method = form.attr('method') || 'post';
            var data = form.serialize();

            self._notify('submitting', {method: method, url: url, data:data});
            $.ajax({
                type: method,
                url: url,
                data: data,
                cache: false,
                crossDomain: true,
                headers: {
                    // make sure request.is_ajax() return True on the server
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).done(function(xhr, textStatus, jqXHR) {

                // update the modal body with the new form
                body.html(xhr);

                // If the server sends back a successful response,
                // we need to further check the HTML received

                // If xhr contains any field errors,
                // the form did not validate successfully,
                // so we keep it open for further editing
                //if ($(xhr).find('.has-error').length > 0) {
                if ($(xhr).find('.has-error').length > 0 || $(xhr).find('.errorlist').length > 0) {
                    self._notify('loaded', {url: url});
                    self._form_ajax_submit();
                } else {
                    // otherwise, we've done and can close the modal
                    self._notify('submitted', {method: method, url: url, data: data});
                    self.close();
                }

            }).fail(function(jqXHR, textStatus, errorThrown) {
                console.log('ERROR: errorThrown=%o, textStatus=%o, jqXHR=%o', errorThrown, textStatus, jqXHR);
                FrontendForms.display_server_error(errorThrown);
            }).always(function() {
                header.removeClass('loading');
            });
        });
    }

We start by taking care of the submit button embedded in the form.
While it's useful and necessary for the rendering of a standalone page, it's
rather disturbing in the modal dialog:

.. figure:: /static/images/form_validation_extra_button.png
   :scale: 80 %

   Can we hide the "Send" button and use the "Save" button from the footer instead ?

Here's the relevant code:

.. code:: javascript

    // use footer save button, if available
    var btn_save = footer.find('.btn-save');
    if (btn_save) {
        form.find('.form-submit-row').hide();
        btn_save.off().on('click', function(event) {
            form.submit();
        });
    }

Then, we proceed by hijacking the form submission:

.. code:: javascript

    // bind to the form’s submit event
    form.on('submit', function(event) {

        // prevent the form from performing its default submit action
        event.preventDefault();

        ...

        var data = form.serialize();
        $.ajax({..., data: data, ...

Finally, we need to detect any form errors after submission, and either
repeat the whole process or close the dialog:

.. code:: javascript

        }).done(function(xhr, textStatus, jqXHR) {

            // update the modal body with the new form
            body.html(xhr);

            if ($(xhr).find('.has-error').length > 0 || $(xhr).find('.errorlist').length > 0) {
                self._form_ajax_submit();
            } else {
                self.close();
            }

One last detail: during content loading, we add a "loading" class to the dialog header,
to make a spinner icon visible until we're ready to either update or close the modal.

.. note::

    Code sample: |link_form-submission|

.. |link_form-submission| raw:: html

   <a href="/samples/form-submission/" target="_blank">Simple Dialogs with Form validation</a>



In the sample project, a sleep of 1 sec has been included in the view to simulate network latency
or a more complex elaboration which might occur in real situations

Using advanced field widgets
----------------------------

Nothing prevents you from using advanced widgets in the form; the only provision is to
rebind all required javascript handlers to the input items after each form submission;
for that, use the `loaded` event.
