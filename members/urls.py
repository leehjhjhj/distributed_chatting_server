from django.urls import path
from members.presentations import SignUpView, SigninView, LogoutView

app_name = 'members'

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('signin/', SigninView.as_view()),
    path('logout/', LogoutView.as_view()),
]