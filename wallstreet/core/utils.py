from .models import *

def checkifvalidIPO(company_id, quantity, offer_bid):
    low_cap = IPO.objects.get(company = company_id).low_cap
    lot_allowed = IPO.objects.get(company = company_id).lot_allowed
    total_volume = IPO.objects.get(company = company_id).total_volume
    if (low_cap < offer_bid and quantity >= lot_allowed and quantity <= total_volume):
        return True
    else:
        return False

def resolve_ipo_allotment():
    ipo = list(IPO.objects.all())
    for ip in ipo:
        ipo = IPO.objects.get(id=ip.id)
        subscriptions = Subscription.objects.filter(company=ipo.company).order_by('-offer_bid')
        total_applied_shares = sum([s.quantity for s in subscriptions])
        total_offer = sum([s.offer_bid for s in subscriptions])
        lots_available = ipo.total_volume // ipo.lot_allowed

        if total_applied_shares > ipo.total_volume:
            final_issue_price = ipo.high_cap 
        else:
            final_issue_price = total_offer // len(list(subscriptions))
        
        shares_allotted = 0
        cash_received = 0
    
        for s in subscriptions:
            if lots_available == 0:
                break
            
            lots_applied = s.quantity // ipo.lot_allowed
    
            lots_allotted = min(lots_available, lots_applied)
            shares_allotted += lots_allotted * ipo.lot_allowed
    
            cash_received += lots_allotted * final_issue_price * ipo.lot_allowed
            profile = Profile.objects.get(user_id = s.user.id)
            profile.no_of_shares += lots_allotted * ipo.lot_allowed
            profile.cash -= lots_allotted * final_issue_price * ipo.lot_allowed
            profile.net_worth += int(profile.no_of_shares * final_issue_price * 0.6 + profile.cash * 0.4)
            profile.save()
    
            ipo.subscribers.add(s.user)
    
            lots_available -= lots_allotted
    
        ipo.final_issue_price = final_issue_price
        ipo.shares_allotted = shares_allotted
        ipo.cash_received = cash_received
        ipo.save()

def PriceTimePriorityAlgorithm():
    buy_orders = list(Transaction.objects.filter(is_buy_type = True))
    sell_orders = list(Transaction.objects.filter(is_buy_type = False))

    buy_orders.sort(key=lambda x: (x.price_placed, x.time_placed), reverse=True)
    sell_orders.sort(key=lambda x: (x.price, x.time))

