from django.db import models


class PollManager(models.Manager):
    def aggregate_count(self):
        return self.all().count()


class PollPermission:
    AGGREGATE_SUMMARY = 'aggregate_summary'


class Poll(models.Model):
    name = models.CharField(max_length=32)
    objects = PollManager()

    class Meta:
        permissions = [
            (PollPermission.AGGREGATE_SUMMARY, 'Can aggregate summary')
        ]
