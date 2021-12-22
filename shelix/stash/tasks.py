import time

from django.utils import timezone

from huey.contrib.djhuey import db_task
from redis.exceptions import LockError

from shelix.stash.models import Log


@db_task()
def process_log_queue(log_id):
    log = Log.objects.filter(id=log_id).first()

    if log:
        lock = log.lock()
        try:
            lock.acquire()

            while 1:
                text = log.pop()
                if not text:
                    break

                log.save_text(text)

                lock.reacquire()
                time.sleep(0.1)

            if log.opened:
                log.logfile.close()

            log.end_ts = timezone.now()
            log.save()
            lock.release()

        except LockError:
            print(f'Lock Not Acquired: {log_id}')
