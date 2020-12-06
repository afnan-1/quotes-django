from django.shortcuts import render
from quote.models import Quote
from .resources import AuthorResource,QuoteResource
from .models import Author
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse
# Create your views here.


def home(request):
    if request.method=="POST":
        if 'myfile' in request.FILES:
            author_resource = AuthorResource
            dataset = Dataset()
            new_author = request.FILES['myfile']
            print('helo')
            if not new_author.name.endswith('xlsx'):
                messages.info(request,'wrong format')
                print('helo0')
                return render(request,'index.html')
            print('hy')
            importted_data = dataset.load(new_author,format='xlsx')
            for data in importted_data:
                dob = data[5]
                dod = data[6]
                attribute = data[8].capitalize()
                sex = data[7].upper()
                value = Author(first_name=data[0], middle_name=data[1], last_name=data[2],alias=data[3],age=data[4],date_of_birth=dob,date_of_death=dod,sex=sex,attribute=attribute,bio=data[9])
                value.save()

        if 'myquotes' in request.FILES:
            quote_resource = QuoteResource
            dataset = Dataset()
            new_Quote = request.FILES['myquotes']
            if not new_Quote.name.endswith('xlsx'):
                messages.info(request,'wrong format please upload in xlsx format')
                return render(request,'index.html')
            importted_data = dataset.load(new_Quote,format='xlsx')
            for data in importted_data:
                print(data[2])
                author = Author.objects.get(full_name=data[2])
                value = Quote(quote=data[0],difficulty=data[1])
                value.save()
                value = Quote.objects.get(pk=value.pk)
                value.author = author
                value.save()
    return render(request,'index.html')