from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Survey
from .serializers import (
    QuestionSerializer,
    PostAnswerSerializer,
)
from .service import (
    get_survey_statistics,
    calculate_response_rate,
    get_ordering_questions,
    get_number_answers,
    get_number_respondents,
    process_user_answer,
)


class SurveyView(APIView):
    """
    Класс для обработки запросов, связанных с прохождением опросов.
    (survey/<int:pk>/) - <int:pk> это номер опроса
    Пример запроса: { "number_answer": 1, "text": "о1" }

    Атрибуты:
    - serializer_class: QuestionSerializer, сериализатор для вопросов опроса.

    Методы:
    - get(self, request, pk):
        Обработчик GET-запроса. Возвращает первый вопрос опроса.

        Параметры:
        - request: Request, объект запроса.
        - pk: int, идентификатор опроса.

        Возвращает:
        - Response: Ответ с данными первого вопроса.

    - post(self, request, pk):
        Обработчик POST-запроса. Обрабатывает ответ пользователя на вопрос и возвращает данные
        для следующего вопроса или сообщение об окончании опроса.

        Параметры:
        - request: Request, объект запроса.
        - pk: int, идентификатор опроса.

        Возвращает:
        - Response: Ответ с данными для следующего вопроса или сообщение об окончании опроса.
    """
    serializer_class = QuestionSerializer

    def get(self, request, pk):
        survey = get_object_or_404(Survey, pk=pk)
        first_question = survey.questions.first()  # первый вопрос
        serializer = self.serializer_class(first_question)
        return Response(serializer.data)

    def post(self, request, pk):
        """
        Обработчик POST-запроса. Обрабатывает ответ пользователя на вопрос и возвращает данные
        для следующего вопроса или сообщение об окончании опроса.

        Параметры:
        - request: Request, объект запроса.
        - pk: int, идентификатор опроса.

        Возвращает:
        - Response: Ответ с данными для следующего вопроса или сообщением об окончании опроса.
        """
        author = self.request.user
        request_data = PostAnswerSerializer(data=request.data)
        survey = get_object_or_404(Survey, pk=pk)
        response_data = process_user_answer(author, request_data, survey)
        return Response(response_data)


class NumberRespondents(APIView):
    """
    Получение общего количества участников опроса по его ID
    (survey/<int:pk>/respondents/  - здесь <int:pk>- это pk опроса)
    """

    def get(self, request, pk):
        """
        Получение общего количества участников опроса.

        Параметры:
        - pk: int, ID опроса.

        Возвращает:
        - JSON-ответ с общим количеством участников опроса.
        """
        result = get_number_respondents(pk)
        return Response(result, status=status.HTTP_200_OK)


class NumberAnswers(APIView):
    """
    Кол-во ответивших и их доля от общего кол-ва участников опроса (например, 95 / 95%)
    (survey/<int:survey_id>/respondents/<int:question_id>/)
    """

    def get(self, request, survey_id: int, question_id: int) -> Response:
        """
        Обработка GET-запроса для получения количества ответивших и их доли от общего количества участников опроса.

        Параметры:
        - survey_id: int, номер опроса.
        - question_id: int, номер вопроса.

        Возвращает:
        - Response: Ответ с результатами запроса.
        """
        response_data = get_number_answers(survey_id, question_id)
        return Response(response_data)


class OrderingQuestions(APIView):
    """
    Порядковый номер вопроса по количеству ответивших.
    Если кол-во совпадает, то и номер должен совпадать.
    (survey/<int:survey_id>/ordering/)
    <int:survey_id> - id опроса
    """

    def get(self, request, survey_id: int) -> Response:
        """
        Обработка GET-запроса для получения порядкового номера вопроса по количеству ответивших.

        Параметры:
        - survey_id: int, номер опроса.

        Возвращает:
        - Response: Ответ с результатами запроса.
        """
        response_data = get_ordering_questions(survey_id)
        return Response(response_data)


class ResponseRate(APIView):
    """
    Класс для подсчета количества выбравших каждый вариант ответа.
    (survey/<int:survey_id>/response_rate/<int:question_id>/)
    <int:survey_id> - id опроса
    <int:question_id> - id вопроса
    """

    def get(self, request, survey_id: int, question_id: int) -> Response:
        """
        Обработка GET-запроса для подсчета количества выбравших каждый вариант ответа.

        Параметры:
        - survey_id: int, номер опроса.
        - question_id: int, номер вопроса.

        Возвращает:
        - Response: Ответ с результатами подсчета.
        """
        response_data = calculate_response_rate(survey_id, question_id)
        return Response(response_data)


class SurveyStatistics(APIView):
    """
    Представление для получения статистики опроса.
    (survey/<int:survey_id>/statistics/)
    <int:survey_id> - id опроса

    Параметры:
    - survey_id (int): Идентификатор опроса.

    Возвращает:
    - Response: JSON-ответ с статистикой опроса.
    """

    def get(self, request, survey_id: int) -> Response:
        """
        Получить статистику опроса.

        Параметры:
        - survey_id (int): Идентификатор опроса.

        Возвращает:
        - Response: JSON-ответ с статистикой опроса.
        """
        try:
            survey_id = int(survey_id)
        except ValueError:
            return Response({"error": "Неверный survey_id"}, status=400)

        response_data = get_survey_statistics(survey_id)
        return Response(response_data)
