from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import QuoteSerializer,QuoteOfTheDay
from .models import Quote,QuoteOfDay
from rest_framework.response import Response
# Create your views here.
@api_view(['GET',])
def quote_list_of_author(request, pk):
    quotes = Quote.objects.filter(author = pk)
    serializer = QuoteSerializer(quotes, many=True)
    return Response(serializer.data)
@api_view(['GET',])
def quote_of_the_day(request):
    quotes = QuoteOfDay.objects.all()
    serializer = QuoteOfTheDay(quotes, many=True)
    return Response(serializer.data)