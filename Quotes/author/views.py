from django.shortcuts import render, redirect
from quote.models import Quote
from .resources import AuthorResource,QuoteResource
from .models import Author,Attribute
from django.contrib import messages
from tablib import Dataset
from .serializers import AuthorSerializer, AuthorListSerializer
from errorlog.models import ErrorMessage
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.views import APIView



# Create your views here.
def home(request):
    return render(request,'index.html')

def admin_import(request):
    if request.method=="POST":
        url_author = '/admin/author/author'
        url_quotes = '/admin/quote/quote'
        url_attribute = '/admin/author/attribute'
        if request.user.is_superuser:
            if 'myfile' in request.FILES:
                author_resource = AuthorResource
                dataset = Dataset()
                new_author = request.FILES['myfile']
                if not new_author.name.endswith('xlsx'):
                    messages.info(request,'wrong format')
                    return render(request,'index.html')
                
                importted_data = dataset.load(new_author,format='xlsx')
                count = len(importted_data.headers)-9
                for data in importted_data:
                    if data is not None:
                        try:
                            data=strip_data(data)
                            dob = data[4]
                            dod = data[5]
                            sex = data[6].upper()
                            if data[1]==None:
                                middle_name = ''
                            else:
                                middle_name=data[1]
                            last_name=data[2]
                            value = Author(first_name=data[0], middle_name=middle_name, last_name=last_name,alias=data[3],date_of_birth=dob,date_of_death=dod,sex=sex,bio=data[-2])
                            value.save()
                            list_attributes = data[7:count+7]
                            add_attribute(value.pk,list_attributes)
                        except Exception as e:
                            error = str(data)+"--"+str(e)
                            err = ErrorMessage(message=error, type_error='Error In Authors')
                            err.save()
                return redirect(url_author)


            elif 'myquotes' in request.FILES:
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
                            data=strip_data(data)
                            try:
                                author = Author.objects.get(full_name=data[2])
                            except:
                                author = Author.objects.get(short_name=data[2])
                            if author:
                                value = Quote(quote=data[0],difficulty=data[1])
                                value.save()
                                value = Quote.objects.get(pk=value.pk)
                                value.author = author
                                value.save()
                        except Exception as e:
                            error = str(data)+"--"+str(e)
                            err = ErrorMessage(message=error, type_error='Error In Quotes')
                            err.save()
                return redirect(url_quotes)

            else: 
                new_attribute = request.FILES['myattributes']
                if not new_attribute.name.endswith('xlsx'):
                    messages.info(request,'wrong format please upload in xlsx format')
                    return render(request,'index.html')
                dataset = Dataset()
                importted_data = dataset.load(new_attribute,format='xlsx')
                for data in importted_data:
                    if data is not None:
                        try:
                            data=strip_data(data)
                            attribute = Attribute(name=data[0])
                            attribute.save()
                        except Exception as e:
                            error = str(data)+"--"+str(e)
                            err = ErrorMessage(message=error, type_error='Error In Quotes')
                            err.save()
                return redirect(url_attribute)

    return render(request,'admin-import.html')


def add_attribute(id,att_list):
    author = Author.objects.get(pk=id)
    for attr in att_list:
        try:
            attr = attr.title()
            attribute_db = Attribute.objects.get(name=attr)
            author.attribute.add(attribute_db)
            author.save()
        except Exception as e:
            pass
def strip_data(data_list):
    stripped_list = []
    for data in data_list:
        if data and isinstance(data,str):
            data=data.strip()
            data=data.title()
        stripped_list.append(data)
    return stripped_list

class AuthorDetails(APIView):
    def get(self,request,pk,*args,**kwargs):
        queryset = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(queryset, many=False,context={"request":request})
        return Response({'data':serializer.data, 'messages':'Authors detail','status':True})


@api_view(['GET',])
def authors_list(request):
    authors = Author.objects.all()
    quotes = Quote.objects.filter(author__in=authors)
    author_quotes = []
    temp =[]
    for i in quotes:
        if i.author not in temp:
            temp.append(i.author)
            author_quotes.append(i.author)
    serializer = AuthorListSerializer(author_quotes, many=True)
    return Response({'data':serializer.data, 'messages':'Authors list','status':True})
