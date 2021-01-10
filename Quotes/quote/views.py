from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import QuoteSerializer
from .models import Quote
from rest_framework.response import Response
# Create your views here.
@api_view(['GET',])
def quote_list_of_author(request, pk):
    quotes = Quote.objects.filter(author = pk)
    serializer = QuoteSerializer(quotes, many=True)
    return Response(serializer.data)
