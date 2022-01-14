import datetime

from django import http
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

import jwt

from shelix.stash.models import Log, LogChunk, LoggingToken


class require_token:
    def __init__(self, target):
        self.target = target

    def __call__(self, request, *args, **kwargs):
        try:
            token = request.POST['token']

        except:
            raise http.Http404

        token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
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


@csrf_exempt
@require_token
def get_log_content(request):
    log_id = request.POST.get('log_id')
    after = request.POST.get('after')

    log = get_object_or_404(Log, id=log_id)
    filters = {'log': log}

    if after:
        try:
            after = datetime.datetime.fromisoformat(after)

        except:
            return http.HttpResponse('Bad Time Format', content_type='text/plain', status_code=400)

        filters['created__gt'] = after

    content = ''
    last_ts = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=60)

    for chunk in LogChunk.objects.filter(**filters).order_by('created')[:100]:
        last_ts = chunk.created

        if chunk.content is None:
            pass

        else:
            content += chunk.content

    resp = http.HttpResponse(content, content_type='text/plain')
    resp['Lastchunk'] = last_ts.isoformat()

    if log.end_ts:
        resp['Endlog'] = log.end_ts.isoformat()

    else:
        resp['Endlog'] = ''

    return resp
