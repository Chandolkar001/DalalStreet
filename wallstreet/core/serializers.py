from rest_framework import serializers 
from .models import *

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    phone = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'phone',
            'first_name',
        ]

    def create(self,data):
        user = User.objects.create(
            username = data['username'],
            email = data['email'],
            first_name=data['first_name'],
        )
        user.set_password(data['password'])
        user.save()
        Profile.objects.update_or_create(user_id = user)
        return user

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "company_name", "short_name", "total_no_shares"]

class IPOSerializer(serializers.ModelSerializer):
    # remove subscribers field during the actual game
    class Meta:
        model = IPO
        fields = ["company", "high_cap", "low_cap", "lot_allowed", "total_volume", "subscribers"]

class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, instance):
        return self.context['request'].user
        
    class Meta:
        model = Subscription
        fields = ["user", "company", "quantity", "offer_bid"]

class SubsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["company", "quantity", "offer_bid"]

class BuyOrderSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, instance):
        return self.context['request'].user
        
    class Meta:
        model = BuyOrder
        fields = ["user", "company", "quantity", "bid_price"]

class SellOrderSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, instance):
        return self.context['request'].user
        
    class Meta:
        model = SellOrder
        fields = ["user", "company", "time_placed", "quantity", "ask_price"]

# ShortOrderSerializer to be implemented

class ShortOrderSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, instance):
        return self.context['request'].user
        
    class Meta:
        model = ShortOrder
        fields = ["user", "company", "time_placed", "quantity", "price","closed_at"]