"""
ASGI config for shelix project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shelix.settings.env')
django.setup()

from shelix.stash.websocket import add_websocket

application = get_asgi_application()
application = add_websocket(application)
