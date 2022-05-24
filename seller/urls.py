from django.urls import path
from . import views

urlpatterns = [
    path("seller_dash/",views.dash, name="dash"),
    path("logout/", views.logoutUser, name="logoutUser"),
    path("products/", views.myproduct, name="myproduct"),
    path("add/", views.addproduct, name="addproduct"),
    path('edit/<int:pid>/',views.edit, name="edit")
]
