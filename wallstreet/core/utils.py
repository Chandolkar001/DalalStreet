from .models import *
from datetime import datetime, timedelta, date
import time

def checkifvalidIPO(company_id, quantity, offer_bid):
    ipo_comp = Company.objects.filter(company_id=company_id).first()
    ipo = IPO.objects.filter(company=company_id).first()
    if date.today() > ipo.closing_date:
        return False
    elif (ipo.low_cap <= offer_bid and offer_bid <= ipo.high_cap and quantity <= ipo.total_volume):
        return True
    else:
        return False

def resolve_ipo_allotment():
    ipo = list(IPO.objects.all())
    for ip in ipo:
        ipo = IPO.objects.get(id=ip.id)
        subscriptions = Subscription.objects.filter(company=ipo.company).order_by('-offer_bid')
        total_applied_lots = sum([s.quantity for s in subscriptions])
        total_applied_shares = total_applied_lots * ipo.lot_size
        total_offer = sum([(s.offer_bid*ipo.lot_size) for s in subscriptions])
        lots_available = ipo.total_volume // ipo.lot_size

        if total_applied_shares > ipo.total_volume:
            final_issue_price = ipo.high_cap 
        else:
            final_issue_price = total_offer / len(list(subscriptions))
        
        shares_allotted = 0
        cash_received = 0
    
        for s in subscriptions:
            if lots_available == 0:
                break
            
            lots_applied = s.quantity 
    
            lots_allotted = min(lots_available, lots_applied)
            shares_allotted += lots_allotted * ipo.lot_size
    
            cash_received += lots_allotted * final_issue_price * ipo.lot_size
            profile = Profile.objects.filter(user_id = s.user).first()
            profile.no_of_shares += lots_allotted * ipo.lot_size
            profile.cash -= lots_allotted * final_issue_price * ipo.lot_size
            profile.net_worth += int(lots_allotted * ipo.lot_size * final_issue_price * 0.6 + profile.cash * 0.4)
            profile.save()
    
            ipo.subscribers.add(s.user)
    
            lots_available -= lots_allotted
    
        ipo.final_issue_price = final_issue_price
        ipo.shares_allotted = shares_allotted
        ipo.cash_received = cash_received
        ipo.save()

orders = []
def add_order(order_type, price, quantity):
    order = {
        "id": len(orders) + 1,
        "type": order_type,
        "price": price,
        "quantity": quantity,
        "timestamp": time.time()
    }
    orders.append(order)

def remove_order(order_id):
    for order in orders:
        if order["id"] == order_id:
            orders.remove(order)
            break

def match_orders():
    # testing code

    # print("Executed")
    # profs = Profile.objects.all()
    # for p in profs:
    #     p.net_worth += 20
    #     p.save()

    # development code

    current_time = datetime.now()
    time_threshold = current_time - timedelta(minutes=10)
    buy_orders = list(BuyOrder.objects.filter(time_placed__gte=time_threshold).order_by('-bid_price'))
    sell_orders = list(SellOrder.objects.filter(time_placed__gte=time_threshold))
    for buy_order in buy_orders:
        for sell_order in sell_orders:
            if sell_order.ask_price == buy_order.bid_price:
                trade_quantity = min(buy_order.quantity, sell_order.quantity)
                trade_price = sell_order.ask_price
                print(f"Trade executed: buy order {buy_order.id} and sell order {sell_order.id} for {trade_quantity} shares at {trade_price}")
                buy_order.quantity -= trade_quantity
                sell_order.quantity -= trade_quantity
                if buy_order.quantity == 0:
                    buy_order.delete()
                else:
                    buy_order.save()
                if sell_order.quantity == 0:
                    sell_order.delete()
                else:
                    sell_order.save()
                buyer = buy_order.user
                seller = sell_order.user
                buyer_profile = Profile.objects.get(user=buyer)
                seller_profile = Profile.objects.get(user=seller)
                buyer_cash_delta = -1 * trade_quantity * trade_price
                seller_cash_delta = trade_quantity * trade_price
                buyer_profile.net_worth -= buyer_cash_delta
                buyer_profile.cash += buyer_cash_delta
                seller_profile.net_worth += seller_cash_delta
                seller_profile.cash -= seller_cash_delta
                buyer.save()
                seller.save()
