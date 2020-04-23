from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('waste_type/', views.select_waste_type, name="waste_type_db"),
    path('apply_info/', views.insert_waste_apply_info, name="apply_info"),
    path('insert_board/', views.insert_board, name="insert_board"),
    path('select_board_title/', views.select_board_title, name="insert_board"),
    path('select_board/', views.select_board, name="insert_board"),

]