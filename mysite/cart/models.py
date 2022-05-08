import random

from django.db import models





type_choices = [
    ('Percents', 'Percents'),
]
class Coupon(models.Model):
    type = models.CharField(max_length=50, blank=True, choices=type_choices)
    discount = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    start = models.DateField(auto_now_add=True)
    end = models.DateField(null=True, blank=True)
    code = models.CharField(max_length=50, unique=True, blank=True)
    is_active = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        self.code = ''.join([random.choice(list('0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')) for x in range(12)])
        super().save(*args, **kwargs)

