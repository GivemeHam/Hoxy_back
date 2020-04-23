from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('waste_type/', views.select_waste_type, name="waste_type_db"),
    path('apply_info/', views.insert_waste_apply_info, name="apply_info"),

]