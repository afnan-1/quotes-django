from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import *
from author.models import Author
from .models import Dataset
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
class listDataSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = DataSetSerializer

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

        # parameter search
        if type_dataset == 'parameter':
            dataset_name = request.data.get('name')
            attributes = request.data.get('attributes')
            size = request.data.get('size')
            gender = request.data.get('gender')
            morality = request.data.get('morality')
            # author = Author.objects.filter(pk__in=authors_id)
            dataset = Dataset(dataset_name=dataset_name, type_dataset=type_dataset, attributes=attributes,size=size,
            gender=gender, morality=morality)
            dataset.save()

        # advance search
        elif type_dataset == 'Manual':
            authors_id = request.data.get('authors')
            author = Author.objects.filter(pk__in=authors_id)
            dataset = Dataset(dataset_name=dataset_name, type_dataset=type_dataset)
            dataset.save()
            for i in author:
                dataset.author.add(i.pk)
        return Response({"message": "Dataset Created", "success": True})
    return Response({"message": "POST Request"})