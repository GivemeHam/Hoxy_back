from django.urls import path
from waste import views

urlpatterns = [
    path("", views.home, name="home"),
]