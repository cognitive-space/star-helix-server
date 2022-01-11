import json
import logging
from importlib import import_module

from asgiref.sync import sync_to_async

from django import http
from django.conf import settings
from django.contrib import auth
from django.core.handlers.asgi import ASGIRequest

from shelix.stash.models import Log, LogChunk

logger = logging.getLogger(__name__)


class AsyncRequest(ASGIRequest):
    def __init__(self, scope, body_file):
        scope['method'] = 'GET'
        super().__init__(scope, body_file)


def init_request(request):
    engine = import_module(settings.SESSION_ENGINE)
    session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
    request.session = engine.SessionStore(session_key)
    request.user = auth.get_user(request)


def add_websocket(app):
    async def websocket_app(scope, receive, send):
        if scope["type"] == "websocket":
            await recv_log_socket(scope, receive, send)
            return

        await app(scope, receive, send)

    return websocket_app


def save_log(data):
    log = Log.objects.filter(id=data['log_id']).first()

    if log:
        chunk = LogChunk(content=data['content'], log=log)
        chunk.save()


async def recv_log_socket(scope, receive, send):
    request = AsyncRequest(scope, None)
    await sync_to_async(init_request, thread_sensitive=True)(request)

    while 1:
        event = await receive()

        if event['type'] == 'websocket.connect':
            logger.info('Websocket Connected')
            await send({'type': 'websocket.accept'})

        elif event['type'] == 'websocket.disconnect':
            logger.error('Websocket Disconnected')
            return

        elif event['type'] == 'websocket.receive':
            data = json.loads(event['text'])
            await sync_to_async(save_log, thread_sensitive=True)(data)
