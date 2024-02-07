from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Survey(models.Model):
    """
    Модель опроса
    """
    title = models.CharField(
        max_length=255,
        verbose_name='Название опроса'
    )
    participants = models.ManyToManyField(
        User,
        related_name='participated_surveys',
        verbose_name='Участники опроса'
    )
    # можно удалить
    total_participants = models.PositiveIntegerField(
        default=0,
        verbose_name='Общее количество участников опроса'
    )
    # можно удалить
    total_responses = models.PositiveIntegerField(
        default=0,
        verbose_name='Общее количество ответивших'
    )
    questions = models.ManyToManyField(
        'Question',
        related_name='surveys_questions',
        verbose_name='Вопросы для опроса'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Question(models.Model):
    """
    Модель вопроса
    """
    text = models.TextField(
        default="Default Text",
        verbose_name='Текст вопроса'
    )
    survey = models.ManyToManyField(
        'Survey',
        related_name='survey_questions',
        verbose_name='Опрос'
    )
    # можно удалить:
    question_processed = models.BooleanField(
        default=False,
        verbose_name='Вопрос обработан'
    )
    answer_group = models.ForeignKey(
        'AnswerGroup',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='questions',
        verbose_name='Группа ответов для вопроса'
    )
    # можно удалить:
    parent_question = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='child_questions',
        verbose_name='Предыдущий вопрос',
        help_text='Если вопрос зависит от предыдущего ответа, выберите предыдущий вопрос.'
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    """
    Модель ответа
    """
    number_answer = models.IntegerField(
        default=1,
        verbose_name='Номер ответа'
    )
    text = models.TextField(
        default="Default Text",
        verbose_name='Текст ответа'
    )
    question = models.ForeignKey(
        Question,
        default=1,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вопрос, к которому относится ответ'
    )
    next_question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='next_question',
        verbose_name='Следующий вопрос',
        help_text='Если ответ влияет на следующий вопрос, выберите следующий вопрос.'
    )
    group = models.ForeignKey(
        "AnswerGroup",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='group_answers',
        verbose_name='Группа, которой принадлежит этот ответ'
    )


    def __str__(self):
        return f"Отвечает {self.text}"

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class AnswerGroup(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название группы ответов'
    )

    def __str__(self):
        return f"Отвечает {self.name}"

    class Meta:
        verbose_name = 'Группа ответов'
        verbose_name_plural = 'Группы ответов'


class UserStatistics(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_statistics',
        verbose_name='Пользователь'
    )
    survey = models.ForeignKey(
        'Survey',
        on_delete=models.CASCADE,
        related_name='user_statistics_survey',
        verbose_name='Опрос'
    )
    questions_shown = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        default=1,
        related_name='user_statistics_questions_shown',
        verbose_name='Показанные вопросы'
    )
    questions_answered = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        default=1,
        related_name='user_statistics_questions_answered',
        verbose_name='Вопросы, на которые ответил'
    )
    answers_given = models.ForeignKey(
        'Answer',
        on_delete=models.CASCADE,
        default=1,
        related_name='user_statistics_answers_given',
        verbose_name='Какими ответами ответил'
    )
    timestamp = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата и время ответа'
    )
    # удалить:
    question_processed = models.BooleanField(
        default=False,
        verbose_name='Вопрос обработан'
    )

    def __str__(self):
        return f"Статистика пользователя {self.user} по опросу {self.survey}"

    class Meta:
        verbose_name = 'Статистика пользователя'
        verbose_name_plural = 'Статистика пользователей'