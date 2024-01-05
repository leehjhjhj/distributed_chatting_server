from django.urls import path
from chats.presentations import (
    ChatView,
    ChatEntryView,
    ChatGetMoreMessageView,
    ChatRoomGetView,
    ChatDetailView,
    ChatJoinedMembersView,
    ChatDeleteView,
    BookmarkView,
)

app_name = 'chats'

urlpatterns = [
    path('create/', ChatView.as_view()),
    path('<str:chat_id>/join/', ChatEntryView.as_view()),
    path('<str:chat_id>/more/', ChatGetMoreMessageView.as_view()),
    path('', ChatRoomGetView.as_view()),
    path('<int:chat_id>/', ChatDetailView.as_view()),
    path('<int:chat_id>/members/', ChatJoinedMembersView.as_view()),
    path('<int:chat_id>/delete/', ChatDeleteView.as_view()),
    path('bookmark/', BookmarkView.as_view()),
]