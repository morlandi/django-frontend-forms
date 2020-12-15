{% verbatim %}

Creating or updating a Django Model (revised)
=============================================

Let's start our optimizations by removing some redundancies.

Sharing a single view for both creating a new specific Model or updating
an existing one is now straitforward; see `edit_artist()` belows:

.. code:: python

    from django.contrib.auth.decorators import login_required
    from django.core.exceptions import PermissionDenied
    from django.http import HttpResponseRedirect
    from frontend_forms.utils import get_object_by_uuid_or_404
    from .forms import ArtistUpdateForm


    @login_required
    def edit_artist(request, pk=None):
        """
        Either add a new Artist,
        or change an existing one
        """

        # Retrieve object
        if pk is None:
            # "Add" mode
            object = None
            required_permission = 'backend.add_artist'
        else:
            # "Change" mode
            object = get_object_by_uuid_or_404(Artist, pk)
            required_permission = 'backend.change_artist'

        # Check user permissions
        if not request.user.is_authenticated or not request.user.has_perm(required_permission):
            raise PermissionDenied


        # Either render only the modal content, or a full standalone page
        if request.is_ajax():
            template_name = 'frontend_forms/generic_form_inner.html'
        else:
            template_name = 'dialogs/generic_form.html'

        if request.method == 'POST':

            form = ArtistUpdateForm(instance=object, data=request.POST)
            if form.is_valid():
                object = form.save()
                if not request.is_ajax():
                    # reload the page
                    if pk is None:
                        message = 'The object "%s" was added successfully.' % object
                    else:
                        message = 'The object "%s" was changed successfully.' % object
                    messages.success(request, message)
                    next = request.META['PATH_INFO']
                    return HttpResponseRedirect(next)
                # if is_ajax(), we just return the validated form, so the modal will close
        else:
            form = ArtistUpdateForm(instance=object)

        return render(request, template_name, {
            'form': form,
            'object': object,
        })


When "pk" is None, we act in `add` mode, otherwise we retrieve the corresponding
object to `change` it.

Both "add" and "change" URL patterns point to the same view,
but the first one doesn’t capture anything from the URL and the default value
of None will be used for `pk`.

.. code:: python

    urlpatterns = [
        ...
        path('artist/add/', views.edit_artist, name="artist-add"),
        path('artist/<uuid:pk>/change/', views.edit_artist, name="artist-change"),
        ...
    ]

We also share a common form:

.. code:: python

    class ArtistEditForm(forms.ModelForm):
        """
        To be used for both creation and update
        """

        class Meta:
            model = Artist
            fields = [
                'description',
                'notes',
            ]

The javascript Dialog can be refactored in a completely generic way,
with no reference to the specific Model in use: infact, it's just a plain dialog
which submits an arbitrary form.

You only need to provide the necessary url (and probably a suitable title)
before opening the dialog:

.. code:: javascript


    <a href="{% url 'samples:artist-add' %}" class="btn btn-primary" onclick="open_artist_edit_dialog(event, 'Create an Artist ...'); return false;">Add</a>
    ...
    {% for artist in artists %}
        ...
        <a href="{% url 'samples:artist-change' artist.id %}" class="btn btn-primary" onclick="open_artist_edit_dialog(event); return false;">Edit</a>
    {% endfor %}


    <script language="javascript">

        function open_artist_edit_dialog(event, title) {
            event.preventDefault();
            var url = $(event.target).attr('href');
            dialog_edit.options.url = url;
            dialog_edit.options.title = title;
            dialog_edit.open(event);
        }

        $(document).ready(function() {

            dialog_edit = new Dialog({
                //url: ...,
                dialog_selector: '#dialog_generic',
                html: '<h1>Loading ...</h1>',
                width: '600px',
                min_height: '200px',
                //title: ...,
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
                            url.searchParams.set('selected_record', object_id);
                            FrontendForms.gotourl(url, show_layer=true);
                            break;
                    }
                }
            });

        });

    </script>


Deleting a Model
----------------

Object deletion can be achieved preparing a view like this:

.. code:: python

    def delete_artist(request, pk):

        required_permission = 'backend.delete_artist'
        if not request.user.is_authenticated or not request.user.has_perm(required_permission):
            raise PermissionDenied

        object = get_object_by_uuid_or_404(Artist, pk)
        object_id = object.id
        object.delete()

        return JsonResponse({'object_id': object_id})

then invoking it via Ajax after user confirmation:

.. code:: html

    <a href="{% url 'samples:artist-delete' artist.id %}" class="btn btn-danger" onclick="delete_artist(event, 'Deleting {{artist.name}}'); return false;">Delete</a>

    <script>
        function delete_artist(event, title) {
            event.preventDefault();
            var url = $(event.target).attr('href');
            FrontendForms.confirmRemoteAction(
                url,
                {
                    title: title,
                    text: 'Are you sure?',
                    confirmButtonClass: 'btn-danger',
                    icon: 'question'
                },
                function(data) {

                    var row = $('tr#artist-'+data.object_id);
                    row.remove();

                    Swal.fire({
                        text: 'Artist "' + data.object_id + '" has been deleted',
                        icon: 'warning'
                    })
                },
                data=true   // set to any value to obtain POST
            );
        }
    </script>

In the above snippet, we use the received object id to remove the corresponding
table row after deletion.

.. note::

    Code sample: |link_edit-a-django-model-revised|

.. |link_edit-a-django-model-revised| raw:: html

   <a href="/samples/edit-a-django-model-revised/" target="_blank">Editing a Django Model (Revised)</a>


{% endverbatim %}
