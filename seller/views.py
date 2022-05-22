from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from main import urls

# Create your views here.

login_required(login_url='login')#user must login to access this page
def dash(request):#dashboard function
    
    return render (request,"dashboard.html")




login_required(login_url='login')#user must login to access this page
def logoutUser(request):#logoutUser function
    logout(request) #logout user
    return redirect("../../") #got back to homepage