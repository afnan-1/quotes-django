from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=20, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
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
    full_name = models.CharField(max_length=100,null= True, blank=True)
    def save( self, *args, **kw ):
        if self.middle_name!=None:
            self.full_name = f'{self.first_name} {self.middle_name} {self.last_name}'
        else:
            self.full_name = f'{self.first_name} {self.last_name}'
        super( Author, self ).save( *args, **kw )
    def __str__(self):
        if self.middle_name!=None:
            return f'{self.first_name} {self.middle_name} {self.last_name}'
        else:
            return f'{self.first_name} {self.last_name}'

    