from django.db import models
from user.models import *
import uuid


class Transaction(models.Model):
    TransactionType = models.TextChoices('TransactionType', 'inflow outflow')
    reference = models.CharField(primary_key=True, max_length=20)
    account = models.CharField(max_length=15)
    date = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=30)
    type = models.CharField(blank=True, choices=TransactionType.choices ,max_length=15)
    category = models.CharField(max_length=15)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )