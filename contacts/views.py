import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from decouple import config  # Для работы с переменными из .env
from .models import Contact

# Функция для отправки сообщения в Telegram
def send_telegram_message(text):
    bot_token = config('TELEGRAM_BOT_TOKEN')  # Получаем токен бота из .env
    chat_id = config('TELEGRAM_CHAT_ID')  # Получаем chat_id из .env
    telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'  # Для форматирования текста в HTML
    }

    try:
        response = requests.post(telegram_api_url, data=payload)
        response.raise_for_status()  # Проверка на успешную отправку
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Проверка на дублирующий запрос
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'Вы уже оставили запрос по этому объекту.')
                return redirect('/listings/' + listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()

        # Отправка сообщения в Telegram
        telegram_message = f"""
        <b>Новый запрос на объект:</b>\n
        <b>Объект:</b> {listing}\n
        <b>Имя:</b> {name}\n
        <b>Email:</b> {email}\n
        <b>Телефон:</b> {phone}\n
        <b>Сообщение:</b> {message}
        """
        send_telegram_message(telegram_message)

        # Сообщение пользователю об успешной отправке
        messages.success(request, 'Ваш запрос был отправлен, риелтор свяжется с вами в ближайшее время.')
        return redirect('/listings/' + listing_id)
