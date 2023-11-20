from django.urls import path
from members.presentations import SignUpView

app_name = 'members'

urlpatterns = [
    path('signup/', SignUpView.as_view())
]