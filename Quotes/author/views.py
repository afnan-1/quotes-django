from django.shortcuts import render, redirect
from quote.models import Quote
from .resources import AuthorResource,QuoteResource
from .models import Author
from django.contrib import messages
from tablib import Dataset
from errorlog.models import ErrorMessage
from django.http import HttpResponse
# Create your views here.


def home(request):
    if request.method=="POST":
        if request.user.is_superuser:
            if 'myfile' in request.FILES:
                author_resource = AuthorResource
                dataset = Dataset()
                new_author = request.FILES['myfile']
                if not new_author.name.endswith('xlsx'):
                    messages.info(request,'wrong format')
                    return render(request,'index.html')
                importted_data = dataset.load(new_author,format='xlsx')
                for data in importted_data:
                    try:
                        dob = data[4]
                        dod = data[5]
                        attribute = data[7].capitalize()
                        sex = data[6].upper()
                        if data[1]==None:
                            middle_name = ''
                        else:
                            middle_name=data[1]
                        if data[2]==None:
                            last_name=''
                        else:
                            last_name=data[2]
                        value = Author(first_name=data[0], middle_name=middle_name, last_name=last_name,alias=data[3],date_of_birth=dob,date_of_death=dod,sex=sex,attribute=attribute,bio=data[8])
                        value.save()
                    except:
                        error = f'First name: {data[0]}, \nMiddle name: {data[1]}, \nLast name: {data[2]}, \nAlias: {data[3]}, \nDob: {data[4]}, \nDod: {data[5]}, \nSex: {data[6]}, \nAttribute: {data[7]}, \nBio: {data[8]}, \nNum of quotes: {data[9]}'
                        err = ErrorMessage(message=error, type_error='Error In Auhtors')
                        err.save()
                return redirect('http://localhost:8000/admin/author/author')


            if 'myquotes' in request.FILES:
                quote_resource = QuoteResource
                dataset = Dataset()
                new_Quote = request.FILES['myquotes']
                if not new_Quote.name.endswith('xlsx'):
                    messages.info(request,'wrong format please upload in xlsx format')
                    return render(request,'index.html')
                importted_data = dataset.load(new_Quote,format='xlsx')
                for data in importted_data:
                    try:
                        author = Author.objects.get(full_name=data[2])
                        if author:
                            value = Quote(quote=data[0],difficulty=data[1])
                            value.save()
                            value = Quote.objects.get(pk=value.pk)
                            value.author = author
                            value.save()
                    except:
                        error = f'Quote: {data[0]},\nDifficulty: {data[1]},\nAuthor: {data[2]}'
                        err = ErrorMessage(message=error, type_error='Error In Quotes')
                        err.save()
                return redirect('http://localhost:8000/admin/quote/quote')
    return render(request,'index.html')