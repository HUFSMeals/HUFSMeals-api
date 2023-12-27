from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        # fields = ['id', 'user', 'rate', 'image', 'title', 'body']
        fields = ['id', 'user', 'rate', 'title', 'body']