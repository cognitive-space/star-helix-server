from django import http
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

import jwt

from shelix.stash.models import Log, LogChunk, LoggingToken


class require_token:
    def __init__(self, target):
        self.target = target

    def __call__(self, request, *args, **kwargs):
        token = request.POST['token']
        token = jwt.decode(token)
        request.token = get_object_or_404(LoggingToken, id=token['id'], active=True)
        return self.target(request, *args, **kwargs)


@csrf_exempt
@require_token
def start_log(request):
    app = request.POST.get('app')

    log = Log(app=app, start_ts=timezone.now())
    log.save()
    return http.JsonResponse({'log_id': log.id})


@csrf_exempt
@require_token
def end_log(request):
    log_id = request.POST.get('log_id')
    log = get_object_or_404(Log, id=log_id)
    log.end_ts = timezone.now()
    log.save()

    return http.JsonResponse({'ended': log.end_ts.isoformat()})


@csrf_exempt
@require_token
def save_log(request):
    log_id = request.POST.get('log_id')
    logs = request.POST.get('logs', '')

    log = get_object_or_404(Log, id=log_id)

    if logs:
        chunk = LogChunk(content=logs, log=log)
        chunk.save()

        return http.JsonResponse({'status': 'received', 'timestamp': chunk.created.isoformat()})

    return http.JsonResponse({'status': 'empty'})
