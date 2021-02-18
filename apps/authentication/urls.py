from django.urls import path, include
# from rest_framework import routers
from .views import RegisterUser, LoginUser

# router = routers.DefaultRouter()
# router.register('register', RegisterUser, basename='RegisterUser')
# router.register('login', LoginUser, basename='LoginUser')

urlpatterns = [
    path('register', RegisterUser.as_view()),
    path('login', LoginUser.as_view())
]
