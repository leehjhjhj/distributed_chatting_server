from django.urls import path
from members.presentations import SignUpView, SigninView

app_name = 'members'

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('signin/', SigninView.as_view()),
]