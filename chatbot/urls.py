from django.urls import path
from .views import whatsapp_reply

urlpatterns = [
    path('whatsapp/', whatsapp_reply, name='whatsapp_reply'),
]
