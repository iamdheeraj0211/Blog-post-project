from django.urls import URLPattern,path
from .views import PostAPIView,RegisterUserView
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns=[path('posts/',PostAPIView.as_view()),
             path('posts/<int:pk>/',PostAPIView.as_view()),
             path('register/',RegisterUserView.as_view()),
             path('login/',obtain_auth_token)]