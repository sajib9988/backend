from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import InquirySerializer
from .models import Inquiry  # ⬅️ এই লাইনটা লাগবে GET এর জন্য

# ✅ POST: Inquiry Create
class InquiryCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ GET: Inquiry List (based on role)
class InquiryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role in ['superadmin', 'admin']:
            inquiries = Inquiry.objects.all()

        elif user.role == 'seller':
            inquiries = Inquiry.objects.filter(property__owner=user)

        elif user.role == 'buyer':
            inquiries = Inquiry.objects.filter(user=user)

        else:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = InquirySerializer(inquiries, many=True)
        return Response(serializer.data)
