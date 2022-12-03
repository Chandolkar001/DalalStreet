from rest_framework import serializers 
from .models import User, Portfolio

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
