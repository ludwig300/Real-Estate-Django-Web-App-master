from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

urlpatterns = [
    path('', views.index, name='listings'),  # Главная страница остается без изменений, т.к. это корневой URL
    path('<int:listing_id>/', views.listing, name='listing'),  # Здесь перевод не нужен, так как ID динамичен
    path(_('search/'), views.search, name='search'),  # Добавляем мультиязычный URL для поиска
]
