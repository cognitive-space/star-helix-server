from django.conf import settings
from django.views import static


def uploads(request, file):
    return static.serve(request, file, document_root=settings.MEDIA_ROOT)
