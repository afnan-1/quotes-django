from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import *
from author.models import Author,Attribute
from .models import Dataset,Question
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import random

# Create your views here.

class DeleteDataSet(generics.DestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = DataSetSerializer


class DatasetView(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DataSetSerializer

@api_view(['GET', 'POST'])
def createDataSet(request):
    if request.method == 'POST':
        type_dataset = request.data.get('type_dataset')
        dataset_name = request.data.get('name')

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
            dataset = Dataset(dataset_name=dataset_name, type_dataset=type_dataset, attributes=attributes,size=size,
            gender=gender, morality=morality)
            dataset.save()
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

        # advance search
        elif type_dataset == 'manual':
            authors_id = request.data.get('authors')
            author = Author.objects.filter(pk__in=authors_id)
            dataset = Dataset(dataset_name=dataset_name, type_dataset=type_dataset)
            dataset.save()
            for i in author:
                dataset.author.add(i.pk)
        return Response({"message": "Dataset Created", "success": True})
    return Response({"message": "POST Request"})

@api_view(['PUT',])
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

class listDataSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DataSetSerializer

@api_view(['GET',])
def list_dataset(request):
    dataset = Dataset.objects.all()
    serializer = DataSetAuthorSerializer(dataset, many=True)
    author_serializer = AuthorDetailSerializer(dataset, many=True)
    return Response({'data':serializer.data,'length':len(author_serializer.data),'message':'Dataset List','status':True})

@api_view(['GET',])
def dataset_authorlist(request):
    dataset = Dataset.objects.all()
    serializer = AuthorDetailSerializer(dataset, many=True)
    return Response({'data':serializer.data,'message':'authors of dataset','status':True})


@api_view(['GET',])
def get_questions(request,pk):
    questions = list(Question.objects.filter(dataset=pk))
    try:
        random_question = random.sample(questions,5)
    except:
        random_question = Question.objects.filter(dataset=pk)
    serializer = QuestionSerializer(random_question, many=True)
    return Response({'data':serializer.data,'message':'Questions of dataset','status':True})