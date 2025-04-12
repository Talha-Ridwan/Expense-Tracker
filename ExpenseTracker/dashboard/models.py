from django.db import models
from mainapp.models import User

class Transactions(models.Model):
    # Umbrella transaction types
    CASH_IN = 'cash_in'
    CASH_OUT = 'cash_out'

    TRANSACTION_TYPES = [
        (CASH_IN, 'Cash In'),
        (CASH_OUT, 'Cash Out'),
    ]

    # Subtypes depending on the type selected
    CASH_IN_SUBTYPES = [
        ('salary', 'Salary'),
        ('gift', 'Gift'),
        ('refund', 'Refund'),
    ]

    CASH_OUT_SUBTYPES = [
        ('purchase', 'Purchase'),
        ('bill', 'Bill'),
        ('donation', 'Donation'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    subtype = models.CharField(max_length=20)  # Choices depend on `type`
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_type_display()} - {self.subtype.capitalize()} - ${self.amount} - {self.timestamp}"
