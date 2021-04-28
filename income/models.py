from django.db import models
from authentication.models import User

class Income(models.Model):
    SOURCE_OPTIONS = [
        ('SALARY', 'SALARY'),
        ('BUSINESS', 'BUSINESS'),
        ('SIDE_HUSTLE', 'SIDE_HUSTLE'),
        ('OTHERS', 'OTHERS'),
    ]

    class Meta:
        ordering: ['-date']

    def __str__(self):
        return str(self.owner)+ 's income'

    source = models.CharField(choices=SOURCE_OPTIONS, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(blank=False, null=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)