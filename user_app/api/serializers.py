from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, min_length=8,
                                             style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'style':
                    {'input_type': 'password'}}

        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(f'could not register  {data["email"]} to {data["username"]}')

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # removes confirm password from validated_data after validation
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainSerializer(TokenObtainSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'username': self.user.username})
        return data
