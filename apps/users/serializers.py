from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Standard Serializer for User Profiles.
    Converts UUIDs and ImageFields to JSON format.
    """
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'profile_pic',
            'bio',
            'balance',
            'is_verified',
            'is_creator'
        ]
        # We make the ID and Balance read-only so they can't be changed via API
        read_only_fields = ['id', 'balance', 'is_verified']

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer specifically for the Signup Process.
    Handles password hashing automatically.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # This creates the user and hashes the password correctly
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserPublicSerializer(serializers.ModelSerializer):
    """
    A 'Lightweight' serializer for showing other users' profiles.
    Hides sensitive data like Email and Balance.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_pic', 'bio', 'is_verified']