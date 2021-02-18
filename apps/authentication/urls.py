from django.urls import path, include
from .views import RegisterUser, LoginUser, UsersList


urlpatterns = [
    path('register', RegisterUser.as_view()),
    path('login', LoginUser.as_view()),
    path('users', UsersList.as_view()),
]
