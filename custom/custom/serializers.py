from rest_framework import serializers
from .models import CustomUser

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email','password','name','userType')
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        
        if not ('.com' in email or  '.edu' in email or '.co' in email ):
            raise serializers.ValidationError("Please check your email")
        
        return attrs
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class getUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email','name','userType')


class LoginUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'password')
    
    def validate(self, attrs):
        print("now")
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        if email is None or email is ' ':
            raise serializers.ValidationError("Email is empty")

        if password is None or password is ' ':
            raise serializers.ValidationError("Password is empty")
        return attrs