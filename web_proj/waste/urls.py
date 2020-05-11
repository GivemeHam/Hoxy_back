from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.home, name="home"),
    path('select_waste_type/', csrf_exempt(views.select_waste_type), name="waste_type_db"),
    path('insert_waste_apply_info/', csrf_exempt(views.insert_waste_apply_info), name="apply_info"),
    path('insert_board/', csrf_exempt(views.insert_board), name="insert_board"),
    path('select_board_title/', csrf_exempt(views.select_board_title), name="select_board_title"),
    path('select_board/', csrf_exempt(views.select_board), name="select_board"),
    path('insert_board_reivew/', csrf_exempt(views.insert_board_review), name="insert_board_review"),
    path('select_board_reivew/', csrf_exempt(views.select_board_reivew), name="select_board_review"),
    path('insert_user_info/', csrf_exempt(views.insert_user_info), name="insert_user_info"),
    path('test/', csrf_exempt(views.test), name="test"),
    #path('index/', csrf_exempt(views.index), name="index"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)