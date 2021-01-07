from django.db import models
from author.models import Author
# Create your models here.
class Dataset(models.Model):
    type_dataset = models.CharField(max_length=50, blank=True, null=True)
    dataset_name = models.CharField(max_length=50, blank=True, null=True)
    morality = models.CharField(max_length=50, blank=True, null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('All','All')
    )
    size = models.IntegerField( blank=True, null=True)
    attributes = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    author = models.ManyToManyField(Author)

    def __str__(self):
        return self.dataset_name