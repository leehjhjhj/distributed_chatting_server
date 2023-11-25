from django.urls import path
from chats.presentations import ChatView, ChatEntryView, ChatGetMoreMessageView

app_name = 'chats'

urlpatterns = [
    path('create/', ChatView.as_view()),
    path('<str:chat_id>/join/', ChatEntryView.as_view()),
    path('<str:chat_id>/more/', ChatGetMoreMessageView.as_view())
]