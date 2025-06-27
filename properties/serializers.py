from rest_framework import serializers
from .models import Property, PropertyImage

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']  # image will store the Cloudinary URL

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'owner', 'title', 'description', 'price', 'location',
            'bedrooms', 'bathrooms', 'space', 'property_type', 'is_published',
            'created_at', 'updated_at', 'images'
        ]
