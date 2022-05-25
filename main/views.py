
from ast import While
import imp
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse
from main import urls
from django.contrib.auth import login, authenticate
from .models import Customusers, categorie, product,cart,Payment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest,HttpResponse
import secrets
from django.conf import settings





def home(request):
    context={}

    #fetching all products
    allpro = product.objects.all()
    context["allpro"]=allpro

    #checking if user wants to delete item from cart
    if "delid" in request.GET:
        delid = request.GET["delid"]
        #getting item to delete from cart
        cart.objects.filter(buyer=Customusers.objects.get(username=request.user.username)).filter(item=product.objects.get(id=delid)).delete()

        return redirect("../")

    #checking which user is logged in
    if request.user.is_authenticated:
        #fetching all cart items for user
        allcartitem = cart.objects.filter(buyer=Customusers.objects.get(username=request.user.username))
        context["allcart"]=allcartitem
        if len(allcartitem)>0:
            totalprice=0
            for c in allcartitem:
                totalprice = totalprice + (c.item.cart_price * c.quantity)
                context["tprice"] = totalprice
        else:
            pass


        if request.user.atype=="seller":
            context["seller"] = "seller"
        if request.user.atype == "buyer":
            context["buyer"] = "buyer"
    else:
        context["none"]= "none"

    #checking if buyer is adding an item to cart
    if "item" in request.GET:
        #checking if user is loggedin
        if request.user.is_authenticated:
            item = request.GET["item"]
            #checking if item is already in cart
            already_added = cart.objects.filter(buyer=Customusers.objects.get(username=request.user.username)).filter(item=product.objects.get(id=item))
            if len(already_added)>0:
                pass
            else:
                #saving item in cart
                cart.objects.create(
                    buyer = Customusers.objects.get(username=request.user.username),
                    item = product.objects.get(id=item)
                )
        else:
            return redirect("../login/")

    #checking if user is increasing item quantity
    if "plus" in request.GET:
        cartid = request.GET["plus"]
        thecart = cart.objects.get(id=cartid)
        #updating the quantity
        thecart.quantity = thecart.quantity + 1
        thecart.save()
        thecart.actual_price = thecart.item.price * thecart.quantity
        thecart.save()
        return redirect("../")

    #checking if user is decreasing item quantity
    if "minus" in request.GET:
        carti = request.GET["minus"]
        tcart = cart.objects.get(id=carti)
        if tcart.quantity >1:
            tcart.quantity = tcart.quantity - 1
            tcart.save()
            tcart.actual_price = tcart.actual_price - tcart.item.price
            tcart.save()
            return redirect("../")
        else:
            pass
    return render(request, "index.html",context)


def register(request):
    if request.method == "POST":
        try:
            name = request.POST["name"]
            type = request.POST["type"]
            email = request.POST["email"]
            password = request.POST["password"]
            cpassword = request.POST["rpassword"]

            if password == cpassword:
                user = Customusers()
                user.username = email
                user.save()
                user.email = email
                user.save()
                user.name = name
                user.save()
                user.atype = type
                user.save()
                user.set_password(cpassword)
                user.save()

                #loggin user in after a successful registration
                auth = authenticate(request, username=email, password=cpassword)
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


@login_required(login_url='signin')
def market(request):
    context={}

    #checking which user is logged in
    if request.user.is_authenticated:
        if request.user.atype=="seller":
            context["seller"] = "seller"
        if request.user.atype == "buyer":
            context["buyer"] = "buyer"
    else:
        context["none"]= "none"

    
    #fetching all cart items for user
    allcartitem = cart.objects.filter(buyer=Customusers.objects.get(username=request.user.username))
    context["allcart"]=allcartitem
    if len(allcartitem)>0:
        totalprice=0
        for c in allcartitem:
            totalprice = totalprice + (c.item.cart_price * c.quantity)
            context["tprice"] = totalprice
    else:
        pass


    if "item" in request.GET:
        #checking if user is loggedin
        item = request.GET["item"]
        #checking if item is already in cart
        already_added = cart.objects.filter(buyer=Customusers.objects.get(username=request.user.username)).filter(item=product.objects.get(id=item))
        if len(already_added)>0:
            pass
        else:
            #saving item in cart
            cart.objects.create(
                buyer = Customusers.objects.get(username=request.user.username),
                item = product.objects.get(id=item)
            )
        
    #checking if user wants to delete item from cart
    if "delid" in request.GET:
        delid = request.GET["delid"]
        #getting item to delete from cart
        cart.objects.filter(buyer=Customusers.objects.get(username=request.user.username)).filter(item=product.objects.get(id=delid)).delete()

        return redirect("../market/")

    #checking for button user clicked from homepage
    if "cat" in request.GET:
        cat = request.GET["cat"]
        if cat=="vegetable":
            vegpro = product.objects.filter(cat="Vegetable")
            if len(vegpro)>0:
                context["allpro"]=vegpro
            else:
                context["notfound"]="No"

        elif cat=="drink":
            drinkpro = product.objects.filter(cat="Drink")
            if len(drinkpro)>0:
                context["allpro"]=drinkpro
            else:
                context["notfound"]="No"

        elif cat=="fish":
            fishpro = product.objects.filter(cat="Fish")
            if len(fishpro)>0:
                context["allpro"]=fishpro
            else:
                context["notfound"]="No"

        elif cat=="sea":
            seapro = product.objects.filter(cat="Sea food")
            if len(seapro)>0:
                context["allpro"]=seapro
            else:
                context["notfound"]="No"

        elif cat=="meat":
            meatpro = product.objects.filter(cat="Meat")
            if len(meatpro)>0:
                context["allpro"]=meatpro
            else:
                context["notfound"]="No"

        elif cat=="dairy":
            dpro = product.objects.filter(cat="Dairy")
            if len(dpro)>0:
                context["allpro"]=dpro
            else:
                context["notfound"]="No"

        elif cat=="fruit":
            fpro = product.objects.filter(cat="Fruit")
            if len(fpro)>0:
                context["allpro"]=fpro
            else:
                context["notfound"]="No"

        elif cat=="spices":
            spro = product.objects.filter(cat="Spices")
            if len(spro)>0:
                context["allpro"]=spro
            else:
                context["notfound"]="No"

        elif cat=="grocery":
            gpro = product.objects.filter(cat="Grocery")
            if len(gpro)>0:
                context["allpro"]=gpro
            else:
                context["notfound"]="No"
    elif request.method=="POST":
        query = request.POST["query"]
        catresult = product.objects.filter(cat__icontains=query)
        titleresult = product.objects.filter(title__icontains=query)
        #combining results together
        allresults = catresult.union(titleresult)
        if len(allresults)>0:
            context["allpro"]=allresults
        else:
            context["notfound"]="No"
    else:
        #fetching all products
        allpro = product.objects.all()
        paginator = Paginator(allpro,10)

        page_number = request.GET.get('page')
        context["allpro"] = paginator.get_page(page_number)

    #checking if user is increasing item quantity
    if "plus" in request.GET:
        cartid = request.GET["plus"]
        thecart = cart.objects.get(id=cartid)
        #updating the quantity
        thecart.quantity = thecart.quantity + 1
        thecart.save()
        thecart.actual_price = thecart.item.price * thecart.quantity
        thecart.save()
        return redirect("../")

    #checking if user is decreasing item quantity
    if "minus" in request.GET:
        carti = request.GET["minus"]
        tcart = cart.objects.get(id=carti)
        if tcart.quantity >1:
            tcart.quantity = tcart.quantity - 1
            tcart.save()
            tcart.actual_price = tcart.actual_price - tcart.item.price
            tcart.save()
            return redirect("../")
        else:
            pass


    return render(request,"market.html",context)



@login_required(login_url='signin')
def checkoutpage(request):
    context={}
    
    #checking which user is logged in
    if request.user.is_authenticated:
        if request.user.atype=="seller":
            context["seller"] = "seller"
        if request.user.atype == "buyer":
            context["buyer"] = "buyer"
    else:
        context["none"]= "none"


     #fetching all cart items for user
    allcartitem = cart.objects.filter(buyer=Customusers.objects.get(username=request.user.username))
    context["allcart"]=allcartitem
    if len(allcartitem)>0:
        totalprice=0
        for c in allcartitem:
            totalprice = totalprice + (c.item.cart_price * c.quantity)
            context["tprice"] = totalprice
    else:
        pass


    #checking if user is increasing item quantity
    if "plus" in request.GET:
        cartid = request.GET["plus"]
        thecart = cart.objects.get(id=cartid)
        #updating the quantity
        thecart.quantity = thecart.quantity + 1
        thecart.save()
        thecart.actual_price = thecart.item.price * thecart.quantity
        thecart.save()
        
        return redirect("../checkoutpage")

    #checking if user is decreasing item quantity
    if "minus" in request.GET:
        carti = request.GET["minus"]
        tcart = cart.objects.get(id=carti)
        if tcart.quantity >1:
            tcart.quantity = tcart.quantity - 1
            tcart.save()
            tcart.actual_price = tcart.actual_price - tcart.item.price
            tcart.save()
            
            return redirect("../checkoutpage")
        else:
            pass

    #checking if user wants to delete item from cart
    if "delid" in request.GET:
        delid = request.GET["delid"]
        #getting item to delete from cart
        cart.objects.filter(buyer=Customusers.objects.get(username=request.user.username)).filter(item=product.objects.get(id=delid)).delete()
        
        return redirect("../checkoutpage")


    

        #fetching all cart items for user
    allcartitem = cart.objects.filter(buyer=Customusers.objects.get(username=request.user.username))
    context["allcart"]=allcartitem
    if len(allcartitem)>0:
        totalprice=0
        for c in allcartitem:
            totalprice = totalprice + (c.item.cart_price * c.quantity)
            context["tprice"] = totalprice
    else:
        pass


    try:
        newPayment = Payment()

        #generating a reference
        while not newPayment.ref:
            ref = secrets.token_urlsafe(10)
            similar_ref = Payment.objects.filter(ref=ref)
            if not similar_ref:
                newPayment.ref = ref

        #multiplying amount by 100
        newamount = int(totalprice) * 100
        print(newamount)

        newPayment.fname = request.user.name
        newPayment.lname = request.user.name
        newPayment.email = request.user.email
        newPayment.amount = totalprice

        newPayment.save()

        context["amount"] = totalprice
        context["ref"] = ref
        context["publicKey"] = settings.PAYSTACK_PK
        context["email"] = request.user.email
        context["amount"] =newamount
        context["disamount"] = totalprice

        context["paynow"] = "paynow"

    except Exception as e:
        print(e)
    

    return render(request,"checkoutpage.html",context)



def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(Payment,ref=ref)
    verified = payment.verify_payment()
    print(verified)
    return redirect('home')

    