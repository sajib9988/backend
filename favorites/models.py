from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from properties.models import Property
 

User = get_user_model()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'property')  

    def __str__(self):
        return f"{self.user} - {self.property}"
