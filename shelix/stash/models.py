from django.db import models


class Log(models.Model):
    app = models.CharField(max_length=75)
    start_ts = models.DateTimeField('Start Timestamp', db_index=True)
    end_ts = models.DateTimeField('End Timestamp', blank=True, null=True)
    logfile = models.FileField(upload_to='logs/%Y/%m/%d/%H')

    class Meta:
        ordering = ['-start_ts']
        index_together = [['start_ts', 'end_ts']]

    def __str__(self):
        return '{} - {}'.format(self.name, self.start_ts.isoformat())
