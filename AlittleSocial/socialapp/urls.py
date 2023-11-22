from django.urls import path, include
from .views import (
    index, login,
    register, logout, single_post
)

urlpatterns = [
    path('', index, name="index"),
    path('login', login, name="login"),
    path('register', register, name="register"),
    path('logout', logout, name="logout"),
    path("post/<str:unique_id>", single_post, name="single_post")
]
