{% verbatim %}

Creating or updating a Django Model in the front-end
====================================================

We can now apply what we've built so far to edit a specific Django model
from the front-end.

Creating a new model
--------------------

This is the view:

.. code:: python

    from django.contrib.auth.decorators import login_required
    from django.core.exceptions import PermissionDenied
    from django.http import HttpResponseRedirect
    from .forms import ArtistCreateForm


    @login_required
    def add_artist(request):

        if not request.user.has_perm('backend.add_artist'):
            raise PermissionDenied

        # Either render only the modal content, or a full standalone page
        if request.is_ajax():
            template_name = 'frontend_forms/generic_form_inner.html'
        else:
            template_name = 'dialogs/generic_form.html'

        object = None
        if request.method == 'POST':

            form = ArtistCreateForm(data=request.POST)
            if form.is_valid():
                object = form.save()
                if not request.is_ajax():
                    # reload the page
                    message = 'The object "%s" was added successfully.' % object
                    messages.success(request, message)
                    next = request.META['PATH_INFO']
                    return HttpResponseRedirect(next)
                # if is_ajax(), we just return the validated form, so the modal will close
        else:
            form = ArtistCreateForm()

        return render(request, template_name, {
            'form': form,
            'object': object,
        })

Note that we're using a generic template from the library called `frontend_forms/generic_form_inner.html`:

.. code:: html

    {% load i18n frontend_forms_tags %}

    <div class="row">
        <div class="col-sm-12">
            <form action="{{ action }}" method="post" class="form {{form.form_class}}" novalidate autocomplete="off">
                {% csrf_token %}
                {% render_form form %}
                <input type="hidden" name="object_id" value="{{ object.id|default:'' }}">
                <div class="form-submit-row">
                    <input type="submit" value="Save" />
                </div>
            </form>
        </div>
    </div>

Chances are we'll reuse it unmodified for other Models as well.

You can of course supply your own template when form rendering needs further customizations.


The form is minimal:

.. code:: python

    from django import forms

    class ArtistCreateForm(forms.ModelForm):

        class Meta:
            model = Artist
            fields = [
                'name',
                'notes',
            ]


On successful creation, we might want to update the user interface;

in the example, for simplicity, we just reload the entire page,
but before doing that we also retrieve the id of the newly created object,
to enhance it after page refresh;

this could be conveniently used, instead, for in-place page updating.

.. code:: javascript

    <script language="javascript">

        dialog_artist_add = new Dialog({
            url: "{% url 'samples:artist-add-basic' %}",
            dialog_selector: '#dialog_generic',
            html: '<h1>Loading ...</h1>',
            width: '600px',
            min_height: '200px',
            title: '<i class="fa fa-calculator"></i> Create an Artist ...',
            button_save_label: "Save",
            button_save_initially_hidden: true,
            enable_trace: true,
            callback: function(event_name, dialog, params) {
                switch (event_name) {
                    case "submitting":
                        FrontendForms.overlay_show('.dialog-body');
                        break;
                    case "loaded":
                        FrontendForms.overlay_hide('.dialog-body');
                        break;
                    case "submitted":
                        var object_id = dialog.element.find('input[name=object_id]').val();
                        // Reload page, with last selection enhanced
                        var url = new URL(document.location.href);
                        url.searchParams.set('selected_artist', object_id);
                        FrontendForms.gotourl(url, show_layer=true);
                        break;
                }
            }
        });

    </script>


Updating an existing object
---------------------------

We treat the update of an existing object in a similar fashion,
but binding the form to the specific database record.

Urls:

.. code:: python

    path('artist/add-basic/', views.add_artist, name="artist-add-basic"),
    path('artist/<uuid:pk>/change-basic/', views.update_artist, name="artist-change-basic"),

The view:

.. code:: python

    from django.contrib.auth.decorators import login_required
    from django.core.exceptions import PermissionDenied
    from django.http import HttpResponseRedirect
    from frontend_forms.utils import get_object_by_uuid_or_404
    from .forms import ArtistUpdateForm


    @login_required
    def update_artist(request, pk):

        if not request.user.has_perm('backend.change_artist'):
            raise PermissionDenied

        # Either render only the modal content, or a full standalone page
        if request.is_ajax():
            template_name = 'frontend_forms/generic_form_inner.html'
        else:
            template_name = 'dialogs/generic_form.html'

        object = get_object_by_uuid_or_404(Artist, pk)
        if request.method == 'POST':

            form = ArtistUpdateForm(instance=object, data=request.POST)
            if form.is_valid():
                object = form.save()
                if not request.is_ajax():
                    # reload the page
                    next = request.META['PATH_INFO']
                    return HttpResponseRedirect(next)
                # if is_ajax(), we just return the validated form, so the modal will close
        else:
            form = ArtistUpdateForm(instance=object)

        return render(request, template_name, {
            'form': form,
            'object': object,
        })

and the form:

.. code:: python

    class ArtistUpdateForm(forms.ModelForm):

        class Meta:
            model = Artist
            fields = [
                'description',
                'notes',
            ]

The Dialog is much similar to the previous one; we just re-initialize it's url
with the required object id before opening it:

.. code:: javascript

    <a href="{% url 'samples:artist-change-basic' artist.id %}" class="btn btn-primary" onclick="open_artist_change_dialog(event); return false;">Edit</a>

    ...

    <script language="javascript">

        function open_artist_change_dialog(event) {
            event.preventDefault();
            var url = $(event.target).attr('href');
            dialog_artist_change.options.url = url;
            dialog_artist_change.open(event);
        }

    </script>

Possible optimizations
----------------------

In the code above, we can detect at list three redundancies:

- the two model forms are identical
- the two views are similar
- and, last but not least, we might try to generalize the views for reuse with any Django model

We'll investigate all these opportunities below;

nonetheless, it's nice to
have a simple snippet available for copy and paste to be used as a starting point
anytime a specific customization is in order.


.. note::

    Code sample: |link_edit-a-django-model-basic|

.. |link_edit-a-django-model-basic| raw:: html

   <a href="/samples/edit-a-django-model-basic/" target="_blank">Editing a Django Model</a>


{% endverbatim %}
