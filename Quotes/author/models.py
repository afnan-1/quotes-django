from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20,blank=True, null=True)
    alias = models.CharField(max_length=1000,blank=True, null=True)
    photo = models.ImageField(upload_to='images/',blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    SEX_CHOICES = (
        ('F', 'Female',),
        ('M', 'Male',),
    )
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        blank=True,
        null=True
    )
    ATTRIBUTE_CHOICES = (
        ('Author','Author'),
        ('Athlete','Athlete'),
        ('Politician','Politician')
    )
    attribute = models.CharField(max_length=10,choices=ATTRIBUTE_CHOICES,blank=True, null=True)
    bio = models.TextField(max_length=500,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " "+ self.last_name