from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

urlpatterns = [
    path(_('login/'), views.login, name='login'),
    path(_('register/'), views.register, name='register'),
    path(_('logout/'), views.logout, name='logout'),
    path(_('dashboard/'), views.dashboard, name='dashboard'),
]
