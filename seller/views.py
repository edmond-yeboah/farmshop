from ast import Try
import imp
from multiprocessing import context
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from main.models import Customusers, categorie,product

from main import urls

# Create your views here.

@login_required(login_url='signin')#user must login to access this page
def dash(request):#dashboard function
    context = {}

    #getting all top products
    toppro = product.objects.filter(seller=Customusers.objects.get(username= request.user.username)).filter(score__gte=3).order_by('-score')
    if len(toppro)>0:
        context["toppro"] = toppro
        context["notnone"] = "notnone"
    else:
        context["none"]="none" 

    #getting all products
    allpro = product.objects.filter(seller=Customusers.objects.get(username=request.user.username))
    context["allpro"] = allpro 
    
    return render (request,"dashboard.html",context)



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

    # if "edit" in request.GET:
    #     eid = request.GET["edit"]
    #     print("Edit was clicked "+ eid)
    
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
            #getting user inputs from html form
            title = request.POST["title"]
            desc = request.POST["desc"]
            sku = request.POST["sku"]
            brand = request.POST["brand"]
            cat = request.POST["cat"]
            price = request.POST["price"]
            imag = request.FILES["img"]

            try:
                product.objects.create( #creating the new product
                    seller = user,
                    title = title,
                    desc = desc,
                    sku = sku,
                    price = price,
                    brand = brand,
                    cat = cat,
                    image = imag,
                )

                return redirect("../products/") #redirecting to products page
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

    return render(request,"addproduct.html",context)



def edit(request,pid):
    context={}

    #getting all categories
    allcat = categorie.objects.all()
    context["allcat"] = allcat

    #getting the product with id
    theproduct = product.objects.get(id=pid)
    if theproduct is not None:
        context["pro"] = theproduct
    else:
        print("Did not get the product")

    #if user clicks on update button
    if request.method == "POST":
        #getting input from html form
        title = request.POST["title"]
        desc = request.POST["desc"]
        sku = request.POST["sku"]
        brand = request.POST["brand"]
        price = request.POST["price"]
        cat = request.POST["cat"]

        #updating product
        theproduct.title = title
        theproduct.desc = desc
        theproduct.sku = sku
        theproduct.brand = brand
        theproduct.price = price
        theproduct.cat = cat

        theproduct.save() #saving product

        return redirect("../../products/") #redirecting to products page
    
    return render(request,"editproduct.html",context)





@login_required(login_url='signin')#user must login to access this page
def logoutUser(request):#logoutUser function
    logout(request) #logout user
    return redirect("../../") #got back to homepage