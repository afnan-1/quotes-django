from django.db import models
import quote
import datetime
# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=20)
    alias = models.CharField(max_length=1000,blank=True, null=True)
    photo = models.ImageField(upload_to='images/',blank=True, null=True)
    date_of_birth = models.DateField()
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
    full_name = models.CharField(max_length=100,unique=True)
    @property
    def num_of_quotes(self):
        return len(quote.models.Quote.objects.filter(author=self.pk))
    @property
    def age( self):

        current = self.date_of_death if self.date_of_death else datetime.date.today()
        return current.year - self.date_of_birth.year - ((current.month,current.day) < (self.date_of_birth.month,self.date_of_birth.day))

    def save(self,*args,**kw):
        if self.middle_name=='':
            self.full_name = f'{self.first_name} {self.last_name}'
        else: 
            self.full_name = f'{self.first_name} {self.middle_name} {self.last_name}'
        super( Author, self ).save( *args, **kw )
    def __str__(self):
        if self.middle_name!=None:
            return f'{self.first_name} {self.middle_name} {self.last_name}'
        else:
            return f'{self.first_name} {self.last_name}'

    
