from django.contrib import admin
from django.urls import path, include
from socket_app.views import test_index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('members/', include("members.urls")),
    path('chats/', include("chats.urls")),
    path('test/<int:chat_id>/', test_index)
]
