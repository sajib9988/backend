# favorites/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Favorite
from .serializers import FavoriteSerializer
from properties.models import Property

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    serializer = FavoriteSerializer(favorites, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request):
    property_id = request.data.get('property')
    
    if not property_id:
        return Response(
            {"error": "Property ID is required to add a favorite."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if property exists
    try:
        property_obj = Property.objects.get(id=property_id)
    except Property.DoesNotExist:
        return Response(
            {"error": "Property not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if favorite already exists
    if Favorite.objects.filter(user=request.user, property=property_obj).exists():
        return Response(
            {"message": "Property is already in your favorites."},
            status=status.HTTP_200_OK
        )
    
    # Create the favorite
    favorite = Favorite.objects.create(
        user=request.user,
        property=property_obj
    )
    
    serializer = FavoriteSerializer(favorite)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favorite(request):
    property_id = request.data.get('property')
    
    if not property_id:
        return Response(
            {"error": "Property ID is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        favorite = Favorite.objects.get(user=request.user, property_id=property_id)
        favorite.delete()
        return Response(
            {"message": "Removed from favorites"},
            status=status.HTTP_204_NO_CONTENT
        )
    except Favorite.DoesNotExist:
        return Response(
            {"error": "Favorite not found"},
            status=status.HTTP_404_NOT_FOUND
        )