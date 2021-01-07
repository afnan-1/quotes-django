from rest_framework import serializers
from author.models import Author
from .models import Dataset
class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields='__all__'