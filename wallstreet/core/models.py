from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class Market(models.Model):
    sensex = models.FloatField(default=0)
    spread = models.IntegerField(default=0)
    bid_range = models.FloatField(default=0)
    market_on = models.BooleanField(default=True)
    start_news = models.BooleanField(default=True)
    news_counter = models.IntegerField(default=0)

class User(AbstractUser):
    phone_no = models.CharField(max_length=10, null=True)

    def __str__(self):
        return str(self.id) + str(self.username)

class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.IntegerField(default=-1)
    cash = models.IntegerField(default=200000)
    net_worth = models.IntegerField(default=0) # 60 % share valuation 40 % cash valuation
    is_hidden = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.user_id.username + "'s Profile"

# Newly edited code for ipo functionality

class Company(models.Model):
# Relevant for both cases -- 
    company_id = models.CharField(max_length=255, default=101, unique=True)
    company_name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=8)
    total_no_shares = models.IntegerField(default=0)
    is_listed = models.BooleanField(default=False)
    listing_price = models.IntegerField(default=0)
    last_traded_price = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.company_name

class IPO(models.Model):
    company = models.ForeignKey(Company, to_field="company_id", on_delete=models.CASCADE)
    high_cap = models.IntegerField(default=0)
    low_cap = models.IntegerField(default=0)
    lot_size = models.IntegerField(default=0)
    total_volume = models.IntegerField(default=0)
    subscribers = models.ManyToManyField(User, blank=True)
    final_issue_price = models.IntegerField(default=0)
    shares_alloted = models.IntegerField(default=0)
    cash_received = models.IntegerField(default=0)
    release_date = models.DateField(default=datetime(2023, 4, 29))
    closing_date = models.DateField(default=datetime(2023, 5, 14))
    red_herring_prospectus = models.URLField(default="https://www.google.com/")
    description = models.TextField(blank=True)


    def __str__(self) -> str:
        return str(self.id)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0) 
    offer_bid = models.IntegerField(default=0)


    def __str__(self):
        return str(self.id)

class BuyOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    time_placed = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    bid_price = models.IntegerField()

    def __str__(self):
        return str(self.id)

class SellOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    time_placed = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    ask_price = models.IntegerField()

    def __str__(self):
        return str(self.id)
    
class UserHistory(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete= models.CASCADE)
    no_of_shares = models.IntegerField(default=0)
    bid_price = models.IntegerField(default=0)
    buy_or_sell = models.BooleanField(default=False)
    transaction_time = models.DateTimeField(auto_now_add=True)

class CompanyShares(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    shares = models.PositiveIntegerField(default=0)



