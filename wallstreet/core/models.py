from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class User(AbstractUser):
    phone_no = models.CharField(max_length=10, null=True)

    def __str__(self):
        return str(self.id) + str(self.username)

class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.IntegerField(default=-1)
    no_of_shares = models.IntegerField(default=0)
    cash = models.IntegerField(default=200000)
    net_worth = models.IntegerField(default=0) # 60 % share valuation 40 % cash valuation
    
    def __str__(self) -> str:
        return self.user_id.username + "'s Profile"

# Newly edited code for ipo functionality

class Company(models.Model):
# Relevant for both cases -- 
    company_name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=8)
    total_no_shares = models.IntegerField(default=0)
    is_listed = models.BooleanField(default=False)
    listing_price = models.IntegerField(default=0)
    last_traded_price = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.company_name

class IPO(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    high_cap = models.IntegerField(default=0)
    low_cap = models.IntegerField(default=0)
    lot_allowed = models.IntegerField(default=0)
    total_volume = models.IntegerField(default=0)
    subscribers = models.ManyToManyField(User, blank=True)
    final_issue_price = models.IntegerField(default=0)
    shares_alloted = models.IntegerField(default=0)
    cash_received = models.IntegerField(default=0)
    release_date = models.DateField(default=datetime(2023, 4, 29))
    closing_date = models.DateField(default=datetime(2023, 5, 14))
    red_herring_prospectus = models.URLField(default="https://www.google.com/")

    def __str__(self) -> str:
        return str(self.id)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0) 
    offer_bid = models.IntegerField(default=0)


    def __str__(self):
        return str(self.id)

# class Stock(models.Model):


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

# # Shorting application to be implemented. 
# class ShortOrder(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     time_placed = models.DateTimeField(auto_now_add=True)
#     quantity = models.IntegerField()
#     # ask_price = models.IntegerField()

#     def __str__(self):
#         return str(self.id)
    
class ShortOrder(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    time_placed = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    # status = models.CharField(max_length=10, default='Open')
    # profit_loss = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.id)



