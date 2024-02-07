from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView


class RegisterUserView(View):
    """
    Вью для регистрации нового пользователя.

    Attributes:
    - template_name (str): Название шаблона для отображения страницы регистрации.
    """
    template_name = 'survey/register.html'

    def get(self, request, *args, **kwargs):
        """
        Обработчик GET-запроса для отображения формы регистрации.

        Returns:
        - HttpResponse: Ответ с отображением формы регистрации.
        """
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """
        Обработчик POST-запроса для обработки данных формы регистрации.

        Returns:
        - HttpResponse: Редирект на страницу home в случае успешной регистрации.
        """
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class HomeView(TemplateView):
    """
    Вью для домашней страницы.

    Attributes:
    - template_name (str): Название шаблона для отображения домашней страницы.
    """
    template_name = 'survey/home.html'

    def get_template_names(self):
        return [self.template_name]
