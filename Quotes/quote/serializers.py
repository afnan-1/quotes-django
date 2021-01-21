from rest_framework import serializers
from .models import Quote
from dataset.models import Question
from author.models import Author
from dataset.serializers import QuestionSerializer
import random

class AuthorSerializer(serializers.ModelSerializer):
    # attribute = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    class Meta:
        model = Author
        fields=('id','full_name',)



class QuoteSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    questions = serializers.SerializerMethodField('get_questions')
    class Meta:
        model = Quote
        fields=('id','author','difficulty','quote','questions')
    def get_questions(self,obj):
        questions = list(Question.objects.all())
        random_questions = random.sample(questions,3)
        q_serializer = QuestionSerializer(random_questions,many=True)
        return q_serializer.data