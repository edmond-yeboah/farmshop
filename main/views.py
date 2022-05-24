
from django.shortcuts import redirect, render
from django.http import HttpResponse
from main import urls
from django.contrib.auth import login, authenticate
from .models import Customusers, categorie




def home(request):
    context={}

    if request.user.is_authenticated:
        if request.user.atype=="seller":
            context["seller"] = "seller"
        if request.user.atype == "buyer":
            context["buyer"] = "buyer"
    else:
        context["none"]= "none"
    return render(request, "index.html",context)

def register(request):
    if request.method == "POST":
        try:
            name = request.POST["name"]
            type = request.POST["type"]
            email = request.POST["email"]
            password = request.POST["password"]
            cpassword = request.POST["rpassword"]

            user = Customusers()
            user.username = email
            user.save()
            user.email = email
            user.save()
            user.atype = type
            user.save()
            user.set_password(cpassword)
            user.save()

            return redirect("../")
            
        except Exception as e:
            print(e)
                                
        
        
        return redirect("../")
    else:
        pass

    return render(request, "register.html")


def signin(request):
    
    if request.user.is_authenticated:
        if request.user.atype == "seller":
            return redirect("../seller_dash/")
        else:
            pass
    if request.method == "POST":
        try:
            email = request.POST["email"]
            passs = request.POST["password"]
            print(passs)

            auth = authenticate(request, username=email, password=passs)
            if auth is not None:
                login(request,auth)
                if request.user.atype=="seller":
                    return redirect("../seller_dash/")
                else:
                    return redirect("../")
            else:
                print("Error loggin in")
        except Exception as e:
            print(e)

    return render(request,"login.html")

    