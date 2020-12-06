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
                dob = data[4]
                dod = data[5]
                attribute = data[7].capitalize()
                value = Author(first_name=data[0],last_name=data[1],alias=data[2],age=data[3],date_of_birth=dob,date_of_death=dod,sex=data[6],attribute=attribute,bio=data[8])
                value.save()

        if 'myquotes' in request.FILES:
            quote_resource = QuoteResource
            dataset = Dataset()
            new_Quote = request.FILES['myquotes']
            print('helo')
            if not new_Quote.name.endswith('xlsx'):
                messages.info(request,'wrong format')
                print('helo0')
                return render(request,'index.html')
            print('hy')
            importted_data = dataset.load(new_Quote,format='xlsx')
            import pdb;pdb.set_trace()
            for data in importted_data:
                print(data[2])
                author = Author.objects.get(first_name=data[2].split(' ')[0], last_name=data[2].split(" ")[1])
                # author = Author.objects.get(first_name="", last_name='nadeem')
                value = Quote(quote=data[0],difficulty=data[1])
                value.save()
                value = Quote.objects.get(quote=data[0])
                value.author = author
                value.save()
    return render(request,'index.html')