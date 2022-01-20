from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    interests = serializers.JSONField() 
    class Meta:
        model = UserProfile
        fields = ['first_name','last_name','account_id','avatar_url', 'address', 'country','interests', 'liked', 'unliked','read','updated_at','created_at']


