
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from myfarm.settings import AUTH_USER_MODEL

# Create your models here

class Customusers(AbstractUser):
    email = models.EmailField(null=True, blank=True, unique=False)
    atype = models.CharField(null=True, blank=True, max_length=30)
    name = models.CharField(null=True, blank=True,max_length=300)
    earning = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.username


class categorie(models.Model):
    name = models.CharField(null=True,blank=True,max_length=300)

    def __str__(self):
        return self.name


class product(models.Model):
    title = models.CharField(null=True,blank=True,max_length=400)
    desc = models.CharField(null=True,blank=True,max_length=700)
    sku = models.CharField(null=True,blank=True,max_length=20)
    brand = models.CharField(null=True,blank=True,max_length=500)
    price = models.IntegerField(null=True,blank=True,default=0)
    image = models.ImageField(upload_to='product_images')
    cat = models.CharField(null=True,blank=True,max_length=20)
    seller = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    score = models.IntegerField(null=True,blank=True,default=0)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class cart(models.Model):
    buyer = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    item = models.ForeignKey(product,on_delete=models.CASCADE)

    def __str__(self):
        return self.buyer.username
