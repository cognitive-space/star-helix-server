import time

from django.db import models
from django.core.files.base import ContentFile

from haikunator import Haikunator

from shelix.stash.queue import log_queue


class Log(models.Model):
    app = models.CharField(max_length=75)
    start_ts = models.DateTimeField('Start Timestamp', db_index=True)
    end_ts = models.DateTimeField('End Timestamp', blank=True, null=True)

    class Meta:
        ordering = ['-start_ts']
        index_together = [['start_ts', 'end_ts']]

    def __str__(self):
        return self.app

    @property
    def open(self):
        if self.end_ts:
            return True

        return False


class LogChunk(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created']
        index_together = [['created', 'log']]

    def __str__(self):
        return '{} - {}'.format(self.log, self.created.isoformat())
