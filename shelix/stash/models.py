import time

from django.db import models
from django.core.files.base import ContentFile

from haikunator import Haikunator

from shelix.stash.queue import log_queue


class Log(models.Model):
    app = models.CharField(max_length=75)
    process = models.CharField(max_length=75, blank=True, null=True)
    start_ts = models.DateTimeField('Start Timestamp', db_index=True)
    end_ts = models.DateTimeField('End Timestamp', blank=True, null=True)
    logfile = models.FileField(upload_to='logs/%Y/%m/%d/%H', blank=True, null=True)

    class Meta:
        ordering = ['-start_ts']
        index_together = [['start_ts', 'end_ts']]

    def __str__(self):
        return '{} - {}'.format(self.name, self.start_ts.isoformat())

    @property
    def key(self):
        return f"logq-{self.id}"

    @property
    def lock_key(self):
        return f"logq-lock-{self.id}"

    def lock(self):
        self._lock = log_queue.client.lock(self.lock_key, timeout=10, blocking_timeout=1)
        return self._lock

    def set_process(self):
        haikunator = Haikunator()

        while 1:
            process = haikunator.haikunate()
            if Log.objects.filter(process=process, app=self.app).count() == 0:
                self.process = process
                break

            time.sleep(0.1)

    def push(self, text):
        if text:
            log_queue.client.rpush(self.key, text)

    def pop(self):
        return log_queue.client.lpop(self.key)

    @property
    def opened(self):
        return getattr(self, '_opened', False)

    @opened.setter
    def opened(self, value):
        self._opened = value

    def save_text(self, text):
        if self.logfile:
            if not self.opened:
                self.logfile.open('ab')
                self.opened = True

            self.logfile.write(text)

        else:
            self.logfile.save(f'{self.app}-{self.id}.log', ContentFile(text))
