from django.urls import path
from .views import list_favorites, add_favorite, remove_favorite

urlpatterns = [
    path('', list_favorites, name='list_favorites'),
    path('add/', add_favorite, name='add_favorite'),
    path('remove/', remove_favorite, name='remove_favorite'),
]
