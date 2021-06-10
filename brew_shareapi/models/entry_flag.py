from django.db import models

class EntryFlag(models.Model):
    reporter = models.ForeignKey('Brewer', related_name='reporter', on_delete=models.DO_NOTHING)
    admin = models.ForeignKey('Brewer', related_name='admin', on_delete=models.DO_NOTHING)
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    resolution = models.CharField(max_length=255)

    class Meta:
        verbose_name = ("entryflag")
        verbose_name_plural = ("entryflags")

