from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_no = models.CharField(max_length=10, null=True)

    def __str__(self):
        return str(self.username)

class Portfolio(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    balance = models.BigIntegerField(default=2000000)

    def __str__(self):
        return str(self.user.username)

# Newly edited code for ipo functionality

class Security(models.Model):
# Relevant for both cases -- 
    security_id = models.IntegerField(null=False)
    security_name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=8)
    total_no_shares = models.IntegerField(default=0)

# is listed shall act as switch to determine if a security is treated as a stock or an ipo
# If false, all the ipo fields are relevant
# If true, all the stock fields are relevant

    is_listed = models.BooleanField(default=False)
    
# IPO Fields
    ipo_lot_min_val = models.IntegerField(default=0)
    ipo_lot_max_val = models.IntegerField(default=0)
    ipo_face_value = models.IntegerField(default=0)
    ipo_lot_size = models.IntegerField(default=0)
# IPO Fields end

# Stock Fields
    listing_price = models.IntegerField(default=0)
    share_price = models.IntegerField(default=0)
# Stock Fields end   
 
    def __str__(self) -> str:
        return self.company_name + '_' + str(self.ipo_face_value if not self.is_listed else self.share_price) + str(self.is_listed)

