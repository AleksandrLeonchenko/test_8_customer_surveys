from typing import Optional, Dict, Union, List
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import connection
from django.db.models import Count

from .models import UserStatistics, Question, Answer, Survey
from .serializers import PostAnswerSerializer


def dictfetchall(cursor):
    """
    Преобразует результаты SQL-запроса в список словарей для удобства использования в Django.

    Параметры:
    - cursor: Объект курсора базы данных.

    Возвращает:
    - List[Dict]: Список словарей, представляющих результаты SQL-запроса.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_survey_statistics(survey_id: int) -> List[Dict[str, Union[str, int]]]:
    """
    Получить статистику опроса.

    Параметры:
    - survey_id (int): Идентификатор опроса.

    Возвращает:
    - List[Dict[str, Union[str, int]]]: Список словарей с статистикой опроса.
    """
    statistics = UserStatistics.objects.filter(
        survey_id=survey_id
    ).values(
        'questions_answered',
        'answers_given'
    ).annotate(
        answer_count=Count('id')
    )

    # Тексты вопросов и ответов:
    questions_text = Question.objects.filter(id__in=[item['questions_answered'] for item in statistics])
    answers_text = Answer.objects.filter(id__in=[item['answers_given'] for item in statistics])

    # Создаем словари для быстрого доступа к текстам вопросов и ответов:
    questions_dict = {question.id: question.text for question in questions_text}
    answers_dict = {answer.id: answer.text for answer in answers_text}

    response_data = []

    for stat in statistics:
        response_data.append({
            'question_text': questions_dict.get(stat['questions_answered'], ''),
            'answer_text': answers_dict.get(stat['answers_given'], ''),
            'answer_count': stat['answer_count'],
        })

    return response_data


def calculate_response_rate(survey_id: int, question_id: int) -> List[Dict]:
    """
    Рассчитывает количества выбравших каждый вариант ответа и общее количество пользователей,
    ответивших на вопрос, в процентном соотношении.

    Параметры:
    - survey_id: int, номер опроса.
    - question_id: int, номер вопроса.

    Возвращает:
    - List[Dict]: Список словарей с информацией о каждом варианте ответа и общем количестве пользователей.
    """
    with connection.cursor() as cursor:
        # Запрос для количества выбравших каждый вариант ответа
        cursor.execute("""
            SELECT
                a.id AS answer_id,
                a.text AS answer_text,
                COUNT(us.id) AS user_count
            FROM
                survey_answer a
            LEFT JOIN
                survey_userstatistics us ON a.id = us.answers_given_id
            WHERE
                us.survey_id = %s
                AND us.questions_answered_id = %s
            GROUP BY
                a.id, a.text
            ORDER BY
                user_count DESC
        """, [survey_id, question_id])

        results = cursor.fetchall()

        # Запрос для общего количества пользователей, ответивших на вопрос
        cursor.execute("""
            SELECT
                COUNT(us.id)
            FROM
                survey_userstatistics us
            WHERE
                us.survey_id = %s
                AND us.questions_answered_id = %s
        """, [survey_id, question_id])

        total_users_count = cursor.fetchone()[0]

    response_data = [
                        {
                            'answer_id': answer[0],
                            'answer_text': answer[1],
                            'user_count': answer[2],
                            'user_percentage': round((answer[2] / total_users_count) * 100,
                                                     2) if total_users_count > 0 else 0,
                        }
                        for answer in results
                    ] + [{'total_users_count': total_users_count}]

    return response_data


def get_ordering_questions(survey_id: int) -> List[Dict]:
    """
    Возвращает порядковый номер вопроса по количеству ответивших.
    Если количество совпадает, то и номер должен совпадать.

    Параметры:
    - survey_id: int, номер опроса.

    Возвращает:
    - List[Dict]: Список словарей с информацией о вопросах и их порядковом номере.
    """
    with connection.cursor() as cursor:
        # Запрос для получения порядкового номера вопроса по количеству ответивших
        cursor.execute("""
            SELECT
                qs.questions_answered_id AS question_id,
                COUNT(qs.id) AS total_users,
                DENSE_RANK() OVER (ORDER BY COUNT(qs.id) DESC) AS rank
            FROM
                survey_userstatistics qs
            WHERE
                qs.survey_id = %s
            GROUP BY
                qs.questions_answered_id
            ORDER BY
                total_users DESC
        """, [survey_id])

        results = dictfetchall(cursor)

    return results


def get_number_answers(survey_id: int, question_id: int) -> Dict:
    """
    Возвращает количество ответивших и их долю от общего количества участников опроса.

    Параметры:
    - survey_id: int, номер опроса.
    - question_id: int, номер вопроса.

    Возвращает:
    - Dict: Словарь с информацией о количестве ответивших и их доле.
    """
    with connection.cursor() as cursor:
        # Подсчитываем количество участников опроса
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) AS total_participants
            FROM survey_survey_participants
            WHERE survey_id = %s
        """, [survey_id])

        row = cursor.fetchone()

        if not row:
            return {"error": "Survey not found"}

        total_participants = row[0]

        # Подсчитываем количество ответивших на вопрос
        cursor.execute("""
            SELECT COUNT(DISTINCT us.user_id) AS total_respondents
            FROM survey_userstatistics us
            WHERE us.survey_id = %s AND us.questions_answered_id = %s
        """, [survey_id, question_id])

        row = cursor.fetchone()

        if not row:
            return {"error": "Question not found"}

        total_respondents = row[0]

        # Рассчитываем долю ответивших от общего количества участников опроса
        percentage_respondents = (total_respondents / total_participants) * 100 if total_participants > 0 else 0

        return {
            "total_respondents": total_respondents,
            "percentage_respondents": f"{percentage_respondents:.2f}%"
        }


def get_number_respondents(survey_id: int) -> Dict:
    """
    Возвращает общее количество участников опроса по его ID.

    Параметры:
    - survey_id: int, номер опроса.

    Возвращает:
    - Dict: Словарь с информацией об общем количестве участников опроса.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) AS total_participants
            FROM survey_survey_participants
            WHERE survey_id = %s
        """, [survey_id])

        row = cursor.fetchone()
        total_participants = row[0] if row else 0

    return {'total_participants': total_participants}


def process_user_answer(
        author,
        request_data: PostAnswerSerializer,
        survey: Survey
) -> Dict[str, Union[str, List[Dict[str, Union[int, str]]]]]:
    """
    Обрабатывает ответ пользователя на вопрос и возвращает данные
    для следующего вопроса или сообщение об окончании опроса.

    Параметры:
    - author: Пользователь, ответивший на вопрос.
    - request_data: Данные ответа пользователя, сериализованные PostAnswerSerializer.
    - survey: Опрос, в рамках которого проходит вопрос.

    Возвращает:
    - response_data: Словарь с данными для следующего вопроса или сообщением об окончании опроса.
    """
    last_user_statistics = UserStatistics.objects.filter(survey=survey).order_by(
        '-timestamp').first()

    if last_user_statistics:
        answers_given_value = last_user_statistics.answers_given
        next_question_value = answers_given_value.next_question
        question_1 = next_question_value
    else:
        question_1 = survey.questions.first()

    if question_1:
        if request_data.is_valid():
            number_answer = request_data.data['number_answer']
            first_question = question_1
            answer = Answer.objects.filter(number_answer=number_answer, group=first_question.answer_group).first()
            user_statistics, created = UserStatistics.objects.update_or_create(
                user=author,
                survey=survey,
                questions_shown=first_question,
                questions_answered=answer.question,
                defaults={"answers_given": answer, "timestamp": timezone.now()}
            )
            if answer.next_question is None:
                response_data = {"message": "Опрос окончен"}
            else:
                next_question = answer.next_question
                next_question_text = next_question.text if next_question else None
                next_question_group = next_question.answer_group if next_question else None
                filtered_answers = next_question_group.group_answers.filter(
                    question=next_question
                ) if next_question_group else []
                response_data = {
                    "вопрос": next_question_text,
                    "ответы": [
                        {"id": answer.id, "текст": answer.text}
                        for answer in filtered_answers
                    ]
                }
        else:
            response_data = {"message": "Неверные данные."}
    else:
        response_data = {"message": "Вопросов нет"}

    return response_data
