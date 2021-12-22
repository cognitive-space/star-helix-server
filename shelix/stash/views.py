from django import http
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from shelix.stash.models import Log
from shelix.stash.tasks import process_log_queue


@csrf_exempt
def start_process(request):
    app = request.POST.get('app')

    log = Log(app=app, start_ts=timezone.now())
    log.set_process()
    log.save()
    return http.JsonResponse({'process': log.process})


@csrf_exempt
def save_log(request):
    app = request.POST.get('app')
    process = request.POST.get('process')
    logs = request.POST.get('logs')

    now = timezone.now()
    log = get_object_or_404(Log, process=process, app=app)
    log.push(logs)

    process_log_queue(log.id)

    return http.JsonResponse({'status': 'received', 'timestamp': now.isoformat()})
