from django.db import models
from authentication.models import User

class Expense(models.Model):
    CATEGORY_OPTIONS = [
        ('ONLINE_SERVICES', 'ONLINE_SERVICES'),
        ('TRAVEL', 'TRAVEL'),
        ('FOOD', 'FOOD'),
        ('RENT', 'RENT'),
        ('TRANSPORT', 'TRANSPORT'),
        ('FEES', 'FEES'),
        ('OTHERS', 'OTHERS')
    ]

    class Meta:
        ordering: ['-date']

    def __str__(self):
        return str(self.owner)+ 's income'

    category = models.CharField(max_length=255, choices=CATEGORY_OPTIONS)
    amount = models.DecimalField(max_digits=10, decimal_places=2, max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False)