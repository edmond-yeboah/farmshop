import email
from statistics import mode
from tkinter import Widget
from django.db import models
from django.forms import PasswordInput
from django.contrib.auth.models import AbstractUser

# Create your models here.
class ToDoList(models.Model):
    name = models.CharField(max_length=200)

    def _str_(self):
        return self.name

class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    complete = models.BooleanField()

class Customer(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email =models.EmailField(max_length=200)
    #Pass = models.CharField(max_length=200,widget=PasswordInput)


    def _str_(self):
        return self.customer_id

class Farmer(models.Model):
    farmer_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email =models.EmailField()
    #Pass = models.CharField(max_length=200,widget=PasswordInput)
    productss = models.CharField(max_length=200)

    def _str_(self):
        return self.farmer_id


class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    quantity = models.FloatField()
    img = models.ImageField()
    product_type = models.CharField(max_length=200)
    farmer = models.ForeignKey(Farmer, null=True, blank=True, on_delete = models.SET_NULL)

    
    def _str_(self):
        return self.product_id

class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete = models.SET_NULL)
    order_id = models.IntegerField(primary_key=True)
    #product_id = models.ForeignKey()

    def __str__(self):
        return self.order_id



class Customusers(AbstractUser):
    email = models.EmailField(null=True, blank=True, unique=False)
    atype = models.CharField(null=True, blank=True, max_length=30)
    name = models.CharField(null=True, blank=True,max_length=300)

    def __str__(self):
        return self.username