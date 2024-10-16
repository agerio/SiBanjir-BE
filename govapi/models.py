from django.db import models

class FloodWatch(models.Model):
    stn_num = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    long = models.DecimalField(max_digits=35, decimal_places=23)
    lat = models.DecimalField(max_digits=35, decimal_places=23)
    hgt = models.FloatField(null=True, blank=True)
    classif = models.CharField(max_length=20, null=True, blank=True)
    obs_time = models.CharField(max_length=20, null=True, blank=True)
    area_id = models.IntegerField()
