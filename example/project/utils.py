import os
from django.db import models


def _remove_file_and_cleanup(filepath):
    """
    Helper to remove a media file;
    also removes the containing folder, if left empty
    """
    folder = os.path.dirname(filepath)
    # remove file
    if os.path.isfile(filepath):
        os.remove(filepath)
    # finally, remove folder if empty
    if os.path.isdir(folder) and len(os.listdir(folder)) <= 0:
        os.rmdir(folder)


def auto_delete_filefields_on_delete(sender, instance, **kwargs):
    """ Deletes file from filesystem when corresponding `MediaFile` object is deleted.
        Adapted: http://stackoverflow.com/questions/16041232/django-delete-filefield

        Connect the receiver as follows:

            models.signals.post_delete.connect(auto_delete_filefields_on_delete, sender=Picture)
    """

    # Collect names of FileFields
    fieldnames = [f.name for f in instance._meta.get_fields() if isinstance(f, models.FileField)]
    for fieldname in fieldnames:
        field = getattr(instance, fieldname)
        if bool(field):
            _remove_file_and_cleanup(field.path)
