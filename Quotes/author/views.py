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
        url = 'http://localhost:8000/admin/author/author'
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
                    if data is not None:
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
                        except Exception as e:
                            error = str(data)+"--"+str(e)
                            err = ErrorMessage(message=error, type_error='Error In Auhtors')
                            err.save()
                return redirect(url)


            if 'myquotes' in request.FILES:
                quote_resource = QuoteResource
                dataset = Dataset()
                new_Quote = request.FILES['myquotes']
                if not new_Quote.name.endswith('xlsx'):
                    messages.info(request,'wrong format please upload in xlsx format')
                    return render(request,'index.html')
                importted_data = dataset.load(new_Quote,format='xlsx')
                for data in importted_data:
                    if data is not None:
                        try:
                            author = Author.objects.get(full_name=data[2])
                            if author:
                                value = Quote(quote=data[0],difficulty=data[1])
                                value.save()
                                value = Quote.objects.get(pk=value.pk)
                                value.author = author
                                value.save()
                        except:
                            error = str(data)+"--"+str(e)
                            err = ErrorMessage(message=error, type_error='Error In Quotes')
                            err.save()
                return redirect(url)
    return render(request,'index.html')