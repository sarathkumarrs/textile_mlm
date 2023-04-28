from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Purchase
from django.utils.timezone import now
import datetime
from decimal import Decimal

# Create your views here.
# utils.py


@login_required
def customer_dashboard(request):
    return render(request, 'customer_dashboard.html', {'customer': request.user.customer})


@login_required
def balance(request):
    # Get the current user's referred users
    referred_users = request.user.referred_users.all()

    # Query for recent transactions by referred users
    recent_transactions = Purchase.objects.filter(user__in=referred_users, created_at__gte=now().date() - datetime.timedelta(days=7))

    # Calculate the cashback for each transaction
    cashback = {}
    for transaction in recent_transactions:
        cashback[transaction.user.username] = transaction.purchase_amount * Decimal('0.05')

    print(cashback)
    return render(request, 'balance.html', {'balance': request.user.balance, 'recent_transactions': recent_transactions, 'cashback': cashback})