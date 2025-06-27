from django.contrib import admin
from .models import Property, PropertyImage

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ('title', 'owner', 'price', 'is_published', 'created_at')
    search_fields = ('title', 'owner__email', 'location')
    list_filter = ('is_published', 'property_type')

admin.site.register(Property, PropertyAdmin)