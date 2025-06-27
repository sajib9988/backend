from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes


class UserListView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ChangeUserRoleView(APIView):
    permission_classes = [IsAuthenticated]  # Only superuser can change role

    def patch(self, request, user_id):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can change roles.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = CustomUser.objects.get(id=user_id)
            new_role = request.data.get('role')
            if new_role not in ['admin', 'agent', 'seller', 'buyer']:
                return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
            user.role = new_role
            user.save()
            return Response({'message': 'Role updated successfully'})
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_user_role(request, user_id):
    if not request.user.is_superuser:
        return Response({'error': 'Only superuser can change roles.'}, status=status.HTTP_403_FORBIDDEN)
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    new_role = request.data.get('role')
    valid_roles = ['admin', 'agent', 'seller', 'buyer']
    if new_role not in valid_roles:
        return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
    user.role = new_role
    user.save()
    return Response({'message': 'Role updated successfully'}, status=status.HTTP_200_OK)
