# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
from .services import distribute_commission

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.TextField()
    bank_account_details = models.TextField()
    referral_code = models.CharField(max_length=255,unique=True, blank=True, editable=False)
    referrer = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referred_users')

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.referral_code:
            # Generate a unique referral code
            referral_code = str(uuid.uuid4())[:8]
            while CustomUser.objects.filter(referral_code=referral_code).exists():
                referral_code = str(uuid.uuid4())[:8]
            self.referral_code = referral_code
        super().save(*args, **kwargs)



class Purchase(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    purchase_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.purchase_amount} - {self.created_at}"

    def save(self, *args, **kwargs):
        if self.purchase_amount >= 500:
            credit_amount = self.purchase_amount * Decimal('0.05')
            self.user.balance += credit_amount
            self.user.save()
        should_distribute_commission = kwargs.pop('distribute_commission', True)
        super().save(*args, **kwargs)
        if should_distribute_commission:
            distribute_commission(self.user, self.purchase_amount)
