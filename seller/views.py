from ast import Try
import imp
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from main.models import Customusers, categorie,product

from main import urls

# Create your views here.

@login_required(login_url='signin')#user must login to access this page
def dash(request):#dashboard function

    if "id" in request.GET:
        idd = request.GET["id"]
        if idd =="1":
            pass
            
    
    return render (request,"dashboard.html")



@login_required(login_url='signin')
def myproduct(request):
    #creating a contex
    context = {}

    #getting all products by logged in seller
    mypro = product.objects.filter(seller = Customusers.objects.get(username=request.user.username))
    if len(mypro)>0:
        context["mypro"] = mypro
        context["notnone"] = "notnone"
    else:
        context["none"] = "none"

    if "edit" in request.GET:
        eid = request.GET["edit"]
        print("Edit was clicked "+ eid)
    
    if "del" in request.GET:
        delid = request.GET["del"]
        #deleting the product
        product.objects.filter(id=delid).delete()

        return redirect("../products/")

    return render(request,"myproducts.html",context)




@login_required(login_url='signin')
def addproduct(request):
    #context
    context = {}
    #getting all categories
    allcat = categorie.objects.all()
    context["allcat"] = allcat

    #checking if a product is submitted
    if request.method=="POST":
        #getting username of the seller
        user = Customusers.objects.get(username=request.user.username)
        try:
            title = request.POST["title"]
            desc = request.POST["desc"]
            sku = request.POST["sku"]
            brand = request.POST["brand"]
            cat = request.POST["cat"]
            price = request.POST["price"]
            imag = request.FILES["img"]

            try:
                product.objects.create(
                    seller = user,
                    title = title,
                    desc = desc,
                    sku = sku,
                    price = price,
                    brand = brand,
                    cat = cat,
                    image = imag,
                )

                return redirect("../products/")
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

    return render(request,"addproduct.html",context)





@login_required(login_url='signin')#user must login to access this page
def logoutUser(request):#logoutUser function
    logout(request) #logout user
    return redirect("../../") #got back to homepage