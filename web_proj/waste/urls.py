from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('waste_type/', views.select_waste_type, name="waste_type_db"),

]