from rest_framework import serializers 
from .models import User, Portfolio, Security

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
        Portfolio.objects.update_or_create(user = user)
        return user

class IPOSerializer(serializers.ModelSerializer):
    class Meta:
        model = Security
        exclude = ["listing_price", "share_price"]

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Security
        exclude = ["ipo_lot_min_value","ipo_lot_max_value","ipo_lot_size","ipo_face_value"]
