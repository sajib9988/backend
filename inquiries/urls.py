from django.urls import path
from .views import InquiryCreateView, InquiryListView

urlpatterns = [
    path('create/', InquiryCreateView.as_view(), name='inquiry-create'),
    path('', InquiryListView.as_view(), name='inquiry-list'),
]
