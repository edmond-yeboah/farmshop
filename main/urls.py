from django.urls import path
from . import views

urlpatterns = [
    #path("<str:name>", views.index, name="index"),
    #path("v1/", views.v1, name="view 1"),
    path("",views.home, name="home"),
    path("register/",views.register, name="register"),
    path("login/",views.signin, name="signin"),
]  