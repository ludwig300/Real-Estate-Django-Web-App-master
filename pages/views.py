from django.shortcuts import render
from django.http import HttpResponse
from listings.choices import price_choices, bedroom_choices

from listings.models import Listing
from realtors.models import Realtor
import logging


# Создаем логгер
logger = logging.getLogger(__name__)


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]

    context = {
        'listings': listings,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices
    }

    return render(request, 'pages/index.html', context)


def about(request):
    # Get all realtors
    realtors = Realtor.objects.order_by('-hire_date')

    # Get MVP
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors
    }

    return render(request, 'pages/about.html', context)


def favorites(request):
    # Получаем параметр favorite_ids из URL
    favorite_ids = request.GET.get('favorite_ids', '')
    logger.info(f"Получен параметр favorite_ids: {favorite_ids}")

    if favorite_ids:
        # Преобразуем строку в список целых чисел, игнорируя пустые элементы
        try:
            favorite_ids_list = [int(id.strip()) for id in favorite_ids.split(',') if id.strip().isdigit()]
            logger.info(f"Список ID избранных объектов после преобразования: {favorite_ids_list}")
        except ValueError as e:
            logger.error(f"Ошибка преобразования ID в числа: {e}")
            favorite_ids_list = []
    else:
        favorite_ids_list = []
        logger.info("Нет ID избранных объектов")

    # Фильтруем объекты Listing по полученным идентификаторам
    listings = Listing.objects.filter(id__in=favorite_ids_list)
    logger.info(f"Количество найденных объектов: {listings.count()}")

    return render(request, 'pages/favorites.html', {'listings': listings})