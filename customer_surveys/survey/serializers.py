from rest_framework import serializers
from .models import Survey, Question, Answer


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['number_answer', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['text', 'answers']


class PostAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['number_answer']
