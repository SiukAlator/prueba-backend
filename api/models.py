from django.db import models


class Scraper(models.Model):
    id = models.AutoField(primary_key = True)
    created_at = models.DateTimeField(auto_now=True)
    currency = models.CharField(max_length = 100)
    frequency = models.IntegerField()
    pass
