from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('room/<int:pk>/',views.room,name="room"),
    path('create-room',views.create_room , name = "create-room"),
    path('update-room/<int:pk>',views.update_room , name = "update-room"),
    path('delete-room/<int:pk>',views.delete_room , name = "delete-room"),
    path('delete-room-confirm/<int:pk>',views.delete_room_confirm , name = "delete-room-confirm"),
    path('login-page/',views.login_page , name = "login-page"),
    path('register-page/',views.register_page , name = "register-page"),
    path('logout-page/',views.logout_page , name = "logout-page"),
    path('delete-message/<int:pk>',views.delete_message , name = "delete-message"),
    path('user-profile/<int:pk>',views.user_profile , name = "user-profile"),
    path('update-user',views.update_user , name = "update-user"),
    path('topics',views.topics , name = "topics"),
    path('activity',views.activity , name = "activity"),
    ]