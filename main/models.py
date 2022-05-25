
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from myfarm.settings import AUTH_USER_MODEL
from .paystack import PayStack

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
    cart_price = models.IntegerField(null=True,blank=True,default=0)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class cart(models.Model):
    buyer = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    item = models.ForeignKey(product,on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True,blank=True,default=1)
    actual_price = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.buyer.username




class Payment(models.Model):
    fname = models.CharField(max_length=200, null=True, blank=True)
    lname = models.CharField(max_length=200, null=True, blank=True)
    amount = models.PositiveIntegerField()
    email = models.EmailField()
    ref = models.CharField(max_length=200)
    status = models.CharField(max_length=200,null=True,blank=True)
    channel = models.CharField(max_length=200,null=True,blank=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fname


    def verify_payment(self):
            paystack = PayStack()
            status, result = paystack.verify_payment(self.ref,self.amount)
            if status:
                if result['amount'] / 100 == self.amount:
                    self.verified = True
                    self.channel = result['channel']
                    self.status = result['status']
                self.save()
            if self.verified:
                    return True, result['amount']
            return False
