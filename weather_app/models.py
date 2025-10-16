from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    search_count = models.PositiveIntegerField(default=0)
    last_temperature = models.FloatField(null=True, blank=True)
    last_description = models.CharField(max_length=200, blank=True, null=True)
    search_count = models.PositiveIntegerField(default=1)  # 📊 necha marta qidirilgan
    searched_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.country})" if self.country else self.name


