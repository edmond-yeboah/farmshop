from django.shortcuts import redirect, render
from django.http import HttpResponse

from main import urls
from .models import ToDoList,Item
from django.contrib.auth import login, authenticate
from .models import Customusers



# Create your views here.

#def index(response, name):
    #ls = ToDoList.objects.get(id=id)
#    return HttpResponse("<h1>Myfarm! %s</h1>"   % name)

#def v1(response):
#    return HttpResponse("<h1>view 1!</h1>") 

def home(request):
    return render(request, "index.html", {})

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

    