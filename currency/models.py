from django.db import models

from django.conf import settings


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True, blank=False)
    nominal = models.IntegerField(default=1)
    title = models.CharField(max_length=60)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    inserted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f'<Currency object: ${self.title}>'
