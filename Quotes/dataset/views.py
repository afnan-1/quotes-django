from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import *
from author.models import Author,Attribute
from .models import Dataset,Question
from user.models import User
from quote.models import Quote
from quote.serializers import QuoteSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json
import random

# Create your views here.


@api_view(['POST',])
# @permission_classes([IsAuthenticated])
def createDataSet(request):
    if request.method == 'POST':
        type_dataset = request.data.get('type_dataset')
        dataset_name = request.data.get('name')
        user_id = User.objects.get(pk=request.user.id)
        gender = []
        if request.data.get('gender') == 'All':
            gender.append('F')
            gender.append('M')
        else:
            gender.append(request.data.get('gender'))
        
        # parameter search
        if type_dataset == 'parameter':
            attributes = request.data.get('attributes')
            print(attributes)
            size = request.data.get('size')
            if size != 'All':
                size = int(size)    
            # gender = request.data.get('gender')
            morality = request.data.get('morality')
            dataset = Dataset(dataset_name=dataset_name,user=user_id ,type_dataset=type_dataset, attributes=attributes,size=size,
            gender=gender, morality=morality)
            dataset.save()
            attribute_id = []
                # filtering attributes from table
            attribute = Attribute.objects.filter(name__in=attributes)
            for i in attribute:
                attribute_id.append(i.pk)
                # filtering authors
            if morality == 'Living':
                if size == 'All':
                    author = Author.objects.filter(sex__in=gender, date_of_death=None, attribute__in=attribute_id)
                else:
                    author = Author.objects.filter(sex__in=gender, date_of_death=None, attribute__in=attribute_id)[:size]
                for i in author:
                    dataset.author.add(i.pk)
            elif morality == 'Deceased':
                if size == 'All':
                    author = Author.objects.filter(sex__in=gender,attribute__in=attribute_id)
                else:
                    author = Author.objects.filter(sex__in=gender,attribute__in=attribute_id)[:size]
                for i in author:
                    if i.date_of_death!=None:
                        # adding authors key to dataset
                        dataset.author.add(i.pk)
            elif morality == 'All':
                if size == 'All':
                    author = Author.objects.filter(sex__in=gender,attribute__in=attribute_id)
                else:
                    author = Author.objects.filter(sex__in=gender,attribute__in=attribute_id)[:size]
                for i in author:
                    dataset.author.add(i.pk)

        # advance search
        elif type_dataset == 'manual':
            authors_id = request.data.get('authors')
            author = Author.objects.filter(pk__in=authors_id)
            dataset = Dataset(dataset_name=dataset_name, user=user_id,type_dataset=type_dataset)
            dataset.save()
            print(user_id.id)
            for i in author:
                dataset.author.add(i.pk)
        return Response({"message": "Dataset Created", "success": True})
    return Response({"message": "POST Request"})

@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def updateDataSet(request,pk):
    if request.method == 'PUT':
        type_dataset = request.data.get('type_dataset')
        dataset_name = request.data.get('name')
        dataset = Dataset.objects.get(pk=pk)
        dataset.dataset_name = dataset_name
        dataset.type_dataset = type_dataset
        gender = []
        if request.data.get('gender') == 'all':
            gender.append('F')
            gender.append('M')
        else:
            gender.append(request.data.get('gender'))
        
        # parameter search
        if type_dataset == 'parameter':
            attributes = request.data.get('attributes')
            size = request.data.get('size')
            if size != 'all':
                size = int(size)    
            # gender = request.data.get('gender')
            morality = request.data.get('morality')
           
            dataset.morality = morality
            dataset.attributes = attributes
            dataset.size = size
            dataset.gender = gender
            # dataset = Dataset(dataset_name=dataset_name, type_dataset=type_dataset, attributes=attributes,size=size,
            # gender=gender, morality=morality)
            dataset.save()
            dataset.author.clear()
            attribute_id = []
                # filtering attributes from table
            attribute = Attribute.objects.filter(name__in=attributes)
            for i in attribute:
                attribute_id.append(i.pk)
                # filtering authors
            if morality == 'living':
                if size == 'all':
                    author = Author.objects.filter(sex__in=gender, date_of_death=None, attribute__in=attribute_id)
                else:
                    author = Author.objects.filter(sex__in=gender, date_of_death=None, attribute__in=attribute_id)[:size]
                for i in author:
                    print(i)
                    dataset.author.add(i.pk)
            elif morality == 'deceased':
                if size == 'all':
                    author = Author.objects.filter(sex__in=gender,attribute__in=attribute_id)
                else:
                    author = Author.objects.filter(sex__in=gender,attribute__in=attribute_id)[:size]
                for i in author:
                    if i.date_of_death!=None:
                        # adding authors key to dataset
                        dataset.author.add(i.pk)
            elif morality == 'all':
                if size == 'all':
                    author = Author.objects.filter(sex__in=gender,attribute__in=attribute_id)
                else:
                    author = Author.objects.filter(sex__in=gender,attribute__in=attribute_id)[:size]
                for i in author:
                    dataset.author.add(i.pk)
        elif type_dataset == 'manual':
            authors_id = request.data.get('authors')
            author = Author.objects.filter(pk__in=authors_id)
            dataset.author.clear()
            dataset.save()
            for i in author:
                dataset.author.add(i.pk)
        return Response({"message":'updated dataset','status':True})
    else:
        return Response({'message':'required POST request','status':False})


@api_view(['GET',])
@permission_classes([IsAuthenticated])
def list_dataset(request):
    user_id = User.objects.get(pk=request.user.id)
    dataset = Dataset.objects.filter(user=user_id).order_by('-created_at')
    serializer = DataSetSerializer(dataset, many=True)
    author_serializer = AuthorDetailSerializer(dataset, many=True)
    return Response({'data':serializer.data,'length':len(author_serializer.data),'message':'Dataset List','status':True})

@api_view(['GET',])
@permission_classes([IsAuthenticated])
def dataset_detail(request,pk):
    dataset = Dataset.objects.get(pk=pk)
    serializer = DataSetSerializer(dataset)
    return Response({'data':serializer.data,'message':'authors of dataset','status':True})


@api_view(['GET',])
# @permission_classes([IsAuthenticated])
def discussion_mode(request,pk):
    dataset = Dataset.objects.get(pk=pk)
    print(dataset.author.all())
    quotations = Quote.objects.filter(author__pk__in=list(dataset.author.all().values_list('id',flat=True)))
    print(len(quotations))
    quotations_serializer = QuoteSerializer(quotations, many=True)
    random_quotations = random.sample(quotations_serializer.data,len(quotations))
    # serializer = QuestionSerializer(random_question, many=True)
    
    return Response({'data':random_quotations,'message':'Questions of dataset','status':True})


@api_view(['DELETE',])
def delete_dataset(request,pk):
    try:
        dataset = Dataset.objects.get(pk=pk).delete()
        return Response({
            'message':"Dataset Delete successfully",
            'status':True
        })
    except:
        return Response({
            'message':'Error',
            'status':False
        })