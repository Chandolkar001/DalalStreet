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
        fields = "__all__"
    
class UserHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    company = CompanySerializer()

    class Meta:
        model = UserHistory
        fields = "__all__"

class CompanyShareSerializer(serializers.ModelSerializer):
    class Meta:
        model= CompanyShares
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    user_history = serializers.SerializerMethodField()
    user_shares = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('rank', 'cash', 'net_worth', 'user_id', 'user_history', 'user_shares')

    def get_user_history(self, obj):
        user_history = UserHistory.objects.filter(user_id=obj.user_id)
        serializer = UserHistorySerializer(user_history, many=True)
        return serializer.data
    
    def get_user_shares(self, obj):
        user_shares = CompanyShares.objects.filter(profile=obj.user_id)
        serializer = CompanyShareSerializer(user_shares, many = True)
        return serializer.data

class IPOSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = IPO
        fields = ["id", "company", "high_cap", "low_cap", "lot_size", "total_volume", "release_date","closing_date","red_herring_prospectus", "description"]

    def get_company_name(self,ipo_obj):
        return ipo_obj.company.company_name

class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, instance):
        return self.context['request'].user
        
    class Meta:
        model = Subscription
        fields = ["user", "company", "quantity", "offer_bid"]

class SubsSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Subscription
        fields = ["company", "quantity", "offer_bid"]

class BuyOrderSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, instance):
        return self.context['request'].user.username
        
    class Meta:
        model = BuyOrder
        fields = ["user", "company", "quantity", "bid_price"]

class SellOrderSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, instance):
        return self.context['request'].user.username
        
    class Meta:
        model = SellOrder
        fields = ["user", "company", "time_placed", "quantity", "ask_price"]

# ShortOrderSerializer to be implemented

# class ShortOrderSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()

#     def get_user(self, instance):
#         return self.context['request'].user
        
#     class Meta:
#         model = ShortOrder
#         fields = ["user", "company", "time_placed", "quantity", "price","closed_at"]