from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница остается без изменений, так как это корневой URL
    path(_('about/'), views.about, name='about'),  # Добавляем мультиязычную поддержку для страницы "О нас"
]
