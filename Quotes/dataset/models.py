from django.db import models
from author.models import Author
from user.models import User
# Create your models here.
class Dataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    type_dataset = models.CharField(max_length=50, blank=True, null=True)
    dataset_name = models.CharField(max_length=50, blank=True, null=True)
    morality = models.CharField(max_length=50, blank=True, null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('All','All')
    )
    size = models.CharField(max_length=10000,blank=True, null=True)
    attributes = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDER_CHOICES)
    author = models.ManyToManyField(Author)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.dataset_name)


class Question(models.Model):
    title = models.TextField(max_length=500)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('All','All')
    )
    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
