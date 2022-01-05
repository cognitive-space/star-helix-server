from django import http
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from shelix.stash.models import Log, LogChunk


@csrf_exempt
def start_log(request):
    app = request.POST.get('app')

    log = Log(app=app, start_ts=timezone.now())
    log.save()
    return http.JsonResponse({'log_id': log.id})


@csrf_exempt
def end_log(request):
    log_id = request.POST.get('log_id')
    log = get_object_or_404(Log, id=log_id)
    log.end_ts = timezone.now()
    log.save()

    return http.JsonResponse({'ended': log.end_ts.isoformat()})


@csrf_exempt
def save_log(request):
    log_id = request.POST.get('log_id')
    logs = request.POST.get('logs', '')

    log = get_object_or_404(Log, id=log_id)

    if logs:
        chunk = LogChunk(content=logs, log=log)
        chunk.save()

        return http.JsonResponse({'status': 'received', 'timestamp': chunk.created.isoformat()})

    return http.JsonResponse({'status': 'empty'})
