
from django.db import models
from django.contrib.auth import get_user_model
from properties.models import Property

User = get_user_model()

class Inquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    message = models.TextField()
    contact_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

# This model represents an inquiry made by a user about a property.
    def __str__(self):
        return f"Inquiry from {self.user.email} on {self.property.title}"
