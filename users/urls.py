from django.urls import path

from users.views import LoginUser, RegisterUser


urlpatterns = [
    path("login", LoginUser.as_view(), name="login"),
    path("register", RegisterUser.as_view(), name="register"),
]
