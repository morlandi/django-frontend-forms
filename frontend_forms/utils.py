import uuid
from django.shortcuts import get_object_or_404
from django.http import Http404


def get_object_by_uuid_or_404(model, uuid_pk):
    """
    Calls get_object_or_404(model, pk=uuid_pk)
    but also prevents "badly formed hexadecimal UUID string" unhandled exception
    """
    if isinstance(uuid_pk, str):
        try:
            uuid.UUID(uuid_pk)
        except Exception as e:
            raise Http404(str(e))
    return get_object_or_404(model, pk=uuid_pk)
