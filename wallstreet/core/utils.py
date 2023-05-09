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
        print(ipo)
        subscriptions = Subscription.objects.filter(company=ipo.company).order_by('-offer_bid')
        total_applied_lots = sum([s.quantity for s in subscriptions])
        total_applied_shares = total_applied_lots * ipo.lot_size
        total_offer = sum([(s.offer_bid*ipo.lot_size) for s in subscriptions])
        lots_available = ipo.total_volume // ipo.lot_size

        if total_applied_shares > ipo.total_volume:
            final_issue_price = ipo.high_cap 
        else:
            final_issue_price = total_offer / (len(list(subscriptions)) * ipo.lot_size)
        print(final_issue_price, total_offer)
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

def match_buy_order(buy_order, sell_orders):
    buy_user = buy_order.user
    buyer = User.filter(user=buy_user)
    # Filter out sell orders with a higher ask price than the bid price of the buy order
    sell_orders = [so for so in sell_orders if so.ask_price <= buy_order.bid_price]
    
    # Sort remaining sell orders by time placed
    sell_orders = sorted(sell_orders, key=lambda so: so.time_placed)
    
    # Match the buy order with the oldest sell order
    for sell_order in sell_orders:
        sell_user = sell_order.user
        seller = User.filter(user=sell_user)
        if buy_order.quantity <= 0:
            break
        if sell_order.quantity <= 0:
            continue
        match_quantity = min(buy_order.quantity, sell_order.quantity)
        buy_order.quantity -= match_quantity
        sell_order.quantity -= match_quantity
        seller.cash += match_quantity*sell_order.ask_price
        buyer.cash -= match_quantity*buy_order.bid_price
        buyer.no_of_shares += match_quantity
        seller.no_of_shares -= match_quantity
        buyer.save()
        seller.save()
    return (sell_orders, buy_order)

def match_sell_order(sell_order, buy_orders):
    sell_user = sell_order.user
    seller = User.filter(user=sell_user)

    # Filter out buy orders with a lower bid price than the ask price of the sell order
    buy_orders = [bo for bo in buy_orders if bo.bid_price >= sell_order.ask_price]
    
    # Sort remaining buy orders by time placed
    buy_orders = sorted(buy_orders, key=lambda bo: bo.time_placed)
    
    # Match the sell order with the oldest buy order
    for buy_order in buy_orders:
        buy_user = buy_order.user
        buyer = User.filter(user=buy_user)
        if sell_order.quantity <= 0:
            break
        if buy_order.quantity <= 0:
            continue
        match_quantity = min(sell_order.quantity, buy_order.quantity)
        sell_order.quantity -= match_quantity
        buy_order.quantity -= match_quantity
        seller.cash += match_quantity*sell_order.ask_price
        buyer.cash -= match_quantity*buy_order.bid_price
        buyer.no_of_shares += match_quantity
        seller.no_of_shares -= match_quantity
        buyer.save()
        seller.save()

    return (buy_orders, sell_order)
def match():
    companies = company.objects.all()
    for company in companies:
        buy_orders = BuyOrder.objects.filter(company=company).order_by('-time_placed')
        sell_orders = SellOrder.objects.filter(company=company).order_by('time_placed')
    while buy_orders and sell_orders:
        sell_orders, buy_order = match_buy_order(buy_orders[0], sell_orders)
        if buy_order.quantity <= 0:
            buy_orders = buy_orders[1:]
        else:
            break
        buy_orders, sell_order = match_sell_order(sell_orders[0], buy_orders)
        if sell_order.quantity <= 0:
            sell_orders = sell_orders[1:]
        else:
            break