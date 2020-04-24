from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.home, name="home"),
    path('waste_type/', csrf_exempt(views.select_waste_type), name="waste_type_db"),
    path('apply_info/', views.insert_waste_apply_info, name="apply_info"),
    path('insert_board/', views.insert_board, name="insert_board"),
    path('select_board_title/', views.select_board_title, name="select_board_title"),
    path('select_board/', views.select_board, name="select_board"),
    path('insert_board_reivew/', views.insert_board_review, name="insert_board_review"),
    path('select_board_reivew/', views.select_board_reivew, name="select_board_review"),
    #path('index/', csrf_exempt(views.index), name="index"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)