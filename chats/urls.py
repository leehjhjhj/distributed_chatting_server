from django.urls import path
from chats.presentations import ChatView
app_name = 'chats'

urlpatterns = [
    path('create/', ChatView.as_view())
]