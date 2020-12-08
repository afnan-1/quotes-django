from django.db import models

# Create your models here.
class ErrorMessage(models.Model):
    message = models.TextField(max_length=5000)
    type_error = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.type_error