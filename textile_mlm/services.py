from decimal import Decimal

def distribute_commission(user, purchase_amount):
    commission_percentages = [0.05, 0.05, 0.05, 0.05, 0.05]
    
    for level, percentage in enumerate(commission_percentages):
        referrer = user.referrer
        if referrer:
            commission_amount = purchase_amount * Decimal(str(percentage))
            referrer.balance += commission_amount
            referrer.save()
            user = referrer
        else:
            break