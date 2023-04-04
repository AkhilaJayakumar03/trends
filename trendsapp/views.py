
import os
import uuid
import datetime
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, logout

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from.forms import *
from.models import *
from django.contrib.auth.models import User
from trendsproject.settings import EMAIL_HOST_USER

# Create your views here.
def index(request):
    return render(request,"index.html")



def shopregister(request):
    if request.method=='POST':
        a=shopregform(request.POST)
        if a.is_valid():
            sn=a.cleaned_data["shopname"]
            sid=a.cleaned_data["shopid"]
            lt=a.cleaned_data["location"]
            em=a.cleaned_data["email"]
            ps=a.cleaned_data["password"]
            cp=a.cleaned_data["confirmpassword"]
            if ps==cp:
                b=shopregmodel(shopname=sn,shopid=sid,location=lt,email=em,password=ps)
                b.save()
                return redirect(shoplogin)
            else:
                messages.success(request,"Password doesn't match")
        else:
            messages.success(request,"Registration failed")
    return render(request,"shopregister.html")


def shoplogin(request):
    if request.method=='POST':
        a=shoplogform(request.POST)
        if a.is_valid():
            em=a.cleaned_data["email"]
            ps=a.cleaned_data["password"]
            request.session['email']=em
            b=shopregmodel.objects.all()
            for i in b:
                if em==i.email and ps==i.password:
                    request.session['id'] = i.id
                    return redirect(shopprofile)
            else:
                messages.success(request,"Login failed")
    return render(request,"shoplogin.html")

def shopprofile(request):
    email=request.session['email']
    return render(request,"shopprofile.html",{'email':email})


def productupload(request):
    if request.method=='POST':
        a=productupform(request.POST,request.FILES)
        id = request.session['id']
        if a.is_valid():
            pn=a.cleaned_data["productname"]
            pr=a.cleaned_data["productprice"]
            ty=a.cleaned_data["producttype"]
            ct=a.cleaned_data["category"]
            ds=a.cleaned_data["description"]
            pm=a.cleaned_data["productimage"]
            b=productupmodel(productname=pn,productprice=pr,producttype=ty,category=ct,description=ds,productimage=pm,shopid=id)
            b.save()
            return redirect(productdisplay)
        else:
            messages.success(request,"product upload failed")
    return render(request,"productupload.html")


def productdisplay(request):
    shpid=request.session['id']
    email=request.session['email']
    a=productupmodel.objects.all()
    pdtnm=[]
    pdtpr=[]
    pdtds=[]
    pdtim=[]
    pdtid=[]
    shopid=[]
    for i in a:
        sid = i.shopid
        shopid.append(sid)
        id=i.id
        pdtid.append(id)
        pm = i.productimage
        pdtim.append(str(pm).split('/')[-1])
        pn=i.productname
        pdtnm.append(pn)
        pr=i.productprice
        pdtpr.append(pr)
        ds=i.description
        pdtds.append(ds)
    mylist=zip(pdtim,pdtnm,pdtpr,pdtds,pdtid,shopid)
    return render(request, "productdisplay.html", {'mylist': mylist,'shpid':shpid,'email':email})

def productdelete(request,id):
    a=productupmodel.objects.get(id=id)
    a.delete()
    return redirect(productdisplay)

def productedit(request,id):
    a=productupmodel.objects.get(id=id)
    im=str(a.productimage).split('/')[-1]
    if request.method=='POST':
        if len(request.FILES):
            if len(a.productimage)>0:
                os.remove(a.productimage.path)
            a.productimage=request.FILES['productimage']
        a.productname=request.POST.get('productname')
        a.productprice=request.POST.get('productprice')
        a.producttype=request.POST.get('producttype')
        a.category=request.POST.get('category')
        a.description=request.POST.get('description')
        a.save()
        return redirect(productdisplay)
    return render(request,"productedit.html",{'a':a,'im':im})


def home(request):
    a=productupmodel.objects.all()
    pdnm=[]
    pdpr=[]
    dscp=[]
    pdimg=[]
    pdid=[]
    for i in a:
        id=i.id
        pdid.append(id)
        pn=i.productname
        pdnm.append(pn)
        pr=i.productprice
        pdpr.append(pr)
        ds=i.description
        dscp.append(ds)
        pm=i.productimage
        pdimg.append(str(pm).split('/')[-1])
    mylist=zip(pdimg,pdnm,pdpr,dscp,pdid)
    return render(request,"home.html",{'mylist':mylist})

def userregister(request):
    if request.method=='POST':
        username=request.POST.get('username')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        if User.objects.filter(username=username).first():
            messages.success(request,"username already taken")
            return redirect(userregister)
        if User.objects.filter(email=email).first():
            messages.success(request,"email already exist")
            return redirect(userregister)
        request.session['email'] = email
        user_obj=User(username=username,first_name=firstname,last_name=lastname,email=email)
        user_obj.set_password(password)
        user_obj.save()
        auth_token=str(uuid.uuid4())
        profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()
        send_mail_reg(email,auth_token)
        return render(request,"success.html")
    return render(request,"userregister.html")



def send_mail_reg(email,auth_token):
    subject='Your account has been verified'
    message=f'Click the link to verify your account http://127.0.0.1:8000/trendsapp/verify/{auth_token}'
    email_from=EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_from,recipient)


def verify(request,auth_token):
    profile_obj=profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,"Your account already verified")
            return redirect(userlogin)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,"Your account has been verified")
        return redirect(userlogin)
    else:
        messages.success(request,"user not found")
        return redirect(userlogin)


def userlogin(request):
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        request.session['username'] = username
        user_obj=User.objects.filter(username=username).first()
        request.session['id'] = user_obj.id
        if user_obj is None:
            messages.success(request,'user not found')
            return redirect(userlogin)
        profile_obj=profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request,'Profile not verified check your mail')
            return redirect(userlogin)
        user=authenticate(username=username,password=password)
        if user is None:
            messages.success(request,'username or password is wrong')
            return redirect(userlogin)
        return redirect(userprofile)
    return render(request,"userlogin.html")


def userprofile(request):
    username=request.session["username"]
    c = datetime.datetime.now()
    return render(request,"userprofile.html",{'c':c,'username':username})


def mendisplay(request):
    pdnm = []
    pdpr = []
    dscp = []
    pdimg = []
    pdid = []
    a=productupmodel.objects.filter(producttype='Men').values()
    for i in a:
        pn = i.get('productname')
        pdnm.append(pn)
        pr = i.get('productprice')
        pdpr.append(pr)
        ds = i.get('description')
        dscp.append(ds)
        pm = i.get('productimage')
        id = i.get('id')
        pdid.append(id)
        pdimg.append(str(pm).split('/')[-1])
    mylist = zip(pdimg, pdnm, pdpr, dscp,pdid)
    return render(request, "men.html",{'mylist':mylist})

def menbag(request):
    pdnm = []
    pdpr = []
    dscp = []
    pdimg = []
    pdid = []
    a=productupmodel.objects.filter(category='Menbags').values()
    for i in a:
        pn = i.get('productname')
        pdnm.append(pn)
        pr = i.get('productprice')
        pdpr.append(pr)
        ds = i.get('description')
        dscp.append(ds)
        pm = i.get('productimage')
        id = i.get('id')
        pdid.append(id)
        pdimg.append(str(pm).split('/')[-1])
    mylist = zip(pdimg, pdnm, pdpr, dscp, pdid)
    return render(request, "menbags.html", {'mylist': mylist})

def menclothing(request):
    pdnm = []
    pdpr = []
    dscp = []
    pdimg = []
    pdid = []
    a=productupmodel.objects.filter(category='Menclothing').values()
    for i in a:
        pn = i.get('productname')
        pdnm.append(pn)
        pr = i.get('productprice')
        pdpr.append(pr)
        ds = i.get('description')
        dscp.append(ds)
        pm = i.get('productimage')
        id = i.get('id')
        pdid.append(id)
        pdimg.append(str(pm).split('/')[-1])
    mylist = zip(pdimg, pdnm, pdpr, dscp, pdid)
    return render(request, "menclothing.html", {'mylist': mylist})

def menwatch(request):
    pdnm = []
    pdpr = []
    dscp = []
    pdimg = []
    pdid = []
    a=productupmodel.objects.filter(category='Menwatches').values()
    for i in a:
        pn = i.get('productname')
        pdnm.append(pn)
        pr = i.get('productprice')
        pdpr.append(pr)
        ds = i.get('description')
        dscp.append(ds)
        pm = i.get('productimage')
        id = i.get('id')
        pdid.append(id)
        pdimg.append(str(pm).split('/')[-1])
    mylist = zip(pdimg, pdnm, pdpr, dscp, pdid)
    return render(request, "menwatch.html", {'mylist': mylist})

def menshoe(request):
    pdnm = []
    pdpr = []
    dscp = []
    pdimg = []
    pdid = []
    a=productupmodel.objects.filter(category='Menshoes').values()
    for i in a:
        pn = i.get('productname')
        pdnm.append(pn)
        pr = i.get('productprice')
        pdpr.append(pr)
        ds = i.get('description')
        dscp.append(ds)
        pm = i.get('productimage')
        id = i.get('id')
        pdid.append(id)
        pdimg.append(str(pm).split('/')[-1])
    mylist = zip(pdimg, pdnm, pdpr, dscp, pdid)
    return render(request, "menshoe.html", {'mylist': mylist})


def womendisplay(request):
    pdnm = []
    pdpr = []
    dscp = []
    pdimg = []
    pdid = []
    a=productupmodel.objects.filter(producttype='Women').values()
    for i in a:
        pn = i.get('productname')
        pdnm.append(pn)
        pr = i.get('productprice')
        pdpr.append(pr)
        ds = i.get('description')
        dscp.append(ds)
        pm = i.get('productimage')
        id = i.get('id')
        pdid.append(id)
        pdimg.append(str(pm).split('/')[-1])
    mylist = zip(pdimg, pdnm, pdpr, dscp,pdid)
    return render(request,"women.html",{'mylist':mylist})


def womenwatch(request):
    pdnm = []
    pdpr = []
    dscp = []
    pdimg = []
    pdid = []
    a=productupmodel.objects.filter(category='Womenwatches').values()
    for i in a:
        pn = i.get('productname')
        pdnm.append(pn)
        pr = i.get('productprice')
        pdpr.append(pr)
        ds = i.get('description')
        dscp.append(ds)
        pm = i.get('productimage')
        id = i.get('id')
        pdid.append(id)
        pdimg.append(str(pm).split('/')[-1])
    mylist = zip(pdimg, pdnm, pdpr, dscp,pdid)
    return render(request,"womenwatch.html",{'mylist':mylist})

def womenclothing(request):
    pdnm = []
    pdpr = []
    dscp = []
    pdimg = []
    pdid = []
    a=productupmodel.objects.filter(category='Womenclothing').values()
    for i in a:
        pn = i.get('productname')
        pdnm.append(pn)
        pr = i.get('productprice')
        pdpr.append(pr)
        ds = i.get('description')
        dscp.append(ds)
        pm = i.get('productimage')
        id = i.get('id')
        pdid.append(id)
        pdimg.append(str(pm).split('/')[-1])
    mylist = zip(pdimg, pdnm, pdpr, dscp,pdid)
    return render(request,"womenclothing.html",{'mylist':mylist})


def womenshoe(request):
    pdnm = []
    pdpr = []
    dscp = []
    pdimg = []
    pdid = []
    a=productupmodel.objects.filter(category='Womenshoes').values()
    for i in a:
        pn = i.get('productname')
        pdnm.append(pn)
        pr = i.get('productprice')
        pdpr.append(pr)
        ds = i.get('description')
        dscp.append(ds)
        pm = i.get('productimage')
        id = i.get('id')
        pdid.append(id)
        pdimg.append(str(pm).split('/')[-1])
    mylist = zip(pdimg, pdnm, pdpr, dscp,pdid)
    return render(request,"womenshoe.html",{'mylist':mylist})

def womenbag(request):
    pdnm = []
    pdpr = []
    dscp = []
    pdimg = []
    pdid = []
    a=productupmodel.objects.filter(category='Womenbags').values()
    for i in a:
        pn = i.get('productname')
        pdnm.append(pn)
        pr = i.get('productprice')
        pdpr.append(pr)
        ds = i.get('description')
        dscp.append(ds)
        pm = i.get('productimage')
        id = i.get('id')
        pdid.append(id)
        pdimg.append(str(pm).split('/')[-1])
    mylist = zip(pdimg, pdnm, pdpr, dscp,pdid)
    return render(request,"womenbag.html",{'mylist':mylist})


def viewallproducts(request):
    email = request.session['email']
    a=productupmodel.objects.all()
    pdnm=[]
    pdpr=[]
    dscp=[]
    pdimg=[]
    for i in a:
        pn=i.productname
        pdnm.append(pn)
        pr=i.productprice
        pdpr.append(pr)
        ds=i.description
        dscp.append(ds)
        pm=i.productimage
        pdimg.append(str(pm).split('/')[-1])
    mylist=zip(pdimg,pdnm,pdpr,dscp)
    return render(request,"viewallproducts.html",{'mylist':mylist,'email':email})

def viewproducts(request):
    username=request.session['username']
    a=productupmodel.objects.all()
    pdnm=[]
    pdpr=[]
    dscp=[]
    pdimg=[]
    pdid=[]
    for i in a:
        id=i.id
        pdid.append(id)
        pn=i.productname
        pdnm.append(pn)
        pr=i.productprice
        pdpr.append(pr)
        ds=i.description
        dscp.append(ds)
        pm=i.productimage
        pdimg.append(str(pm).split('/')[-1])
    mylist=zip(pdimg,pdnm,pdpr,dscp,pdid)
    return render(request,"viewproducts.html",{'mylist':mylist,'username':username})


def addtocart(request,id):
    a=productupmodel.objects.get(id=id)
    c = request.session['id']
    if cart.objects.filter(productname=a.productname):
        return render(request,"itemalreadyincart.html")
    b=cart(productname=a.productname,productprice=a.productprice,description=a.description,productimage=a.productimage,userid=c)
    b.save()
    return redirect(cartdisplay)

def cartdisplay(request):
    usid = request.session['id']
    a = cart.objects.all()
    pdtnm = []
    pdtpr = []
    pdtds = []
    pdtim = []
    pdtid = []
    userid=[]
    for i in a:
        uid = i.userid
        userid.append(uid)
        id = i.id
        pdtid.append(id)
        pm = i.productimage
        pdtim.append(str(pm).split('/')[-1])
        pn = i.productname
        pdtnm.append(pn)
        pr = i.productprice
        pdtpr.append(pr)
        ds = i.description
        pdtds.append(ds)
    mylist = zip(pdtim, pdtnm, pdtpr, pdtds, pdtid,userid)
    return render(request, "cartdisplay.html", {'mylist': mylist,'usid':usid})

def cartitemremove(request,id):
    a=cart.objects.get(id=id)
    a.delete()
    return redirect(cartdisplay)


def addtowishlist(request,id):
    a=productupmodel.objects.get(id=id)
    c = request.session['id']
    if wishlist.objects.filter(productname=a.productname):
        return render(request,"itemalreadyinwishlist.html")
    else:
        b=wishlist(productname=a.productname,productprice=a.productprice,description=a.description,productimage=a.productimage,userid=c)
        b.save()
        return redirect(wishlistdisplay)

def wishlistdisplay(request):
    usid = request.session['id']
    a = wishlist.objects.all()
    pdtnm = []
    pdtpr = []
    pdtds = []
    pdtim = []
    pdtid = []
    userid=[]
    for i in a:
        uid = i.userid
        userid.append(uid)
        id = i.id
        pdtid.append(id)
        pm = i.productimage
        pdtim.append(str(pm).split('/')[-1])
        pn = i.productname
        pdtnm.append(pn)
        pr = i.productprice
        pdtpr.append(pr)
        ds = i.description
        pdtds.append(ds)
    mylist = zip(pdtim, pdtnm, pdtpr, pdtds, pdtid,userid)
    return render(request, "wishlistdisplay.html", {'mylist': mylist,'usid':usid})

def wishitemremove(request,id):
    a=wishlist.objects.get(id=id)
    a.delete()
    return redirect(wishlistdisplay)

def wishtocart(request,id):
    c = request.session['id']
    a=wishlist.objects.get(id=id)
    if cart.objects.filter(productname=a.productname):
        return render(request,"itemalreadyincart.html")
    else:
        b=cart(productname=a.productname,productprice=a.productprice,description=a.description,productimage=a.productimage,userid=c)
        b.save()
        return redirect(cartdisplay)



def buyproduct(request,id):
    a=cart.objects.get(id=id)
    im=str(a.productimage).split('/')[-1]
    if request.method=='POST':
        pn=request.POST.get('productname')
        pr=request.POST.get('productprice')
        ds=request.POST.get('description')
        qt=request.POST.get('quantity')
        b=buy(productname=pn,productprice=pr,description=ds,quantity=qt)
        b.save()
        total=int(pr)*int(qt)
        return render(request,"finalbill.html",{'im':im,'pn':pn,'pr':pr,'ds':ds,'qt':qt,'total':total})
    return render(request,"buy.html",{'a':a,'im':im})


def payment(request):
    if request.method=='POST':
        cardnumber = request.POST.get('cardnumber')
        holdername = request.POST.get('holdername')
        expire = request.POST.get('expire')
        ccv = request.POST.get('ccv')
        b = cardmodels(cardnumber=cardnumber,holdername=holdername,expire=expire,ccv=ccv)
        b.save()
        c=datetime.date.today()
        d=c+timedelta(15)
        return render(request, "orderplaced.html",{'d':d})
    return render(request,"payment.html")

def shopnotification(request):
    email=request.session['email']
    a=shopnotify.objects.all()
    cn=[]
    dt=[]
    usid=[]
    for i in a:
        content=i.content
        cn.append(content)
        date = i.date
        dt.append(date)
        id=i.id
        usid.append(id)
    mylist=zip(cn,dt,usid)
    return render(request,"shopnoti.html",{'mylist':mylist,'email':email})

def usernotification(request):
    username=request.session['username']
    a=usernotify.objects.all()
    cn=[]
    dt=[]
    usid=[]
    for i in a:
        content=i.content
        cn.append(content)
        date = i.date
        dt.append(date)
        id=i.id
        usid.append(id)
    mylist=zip(cn,dt,usid)
    return render(request,"usernoti.html",{'mylist':mylist,'username':username})

def user_logout(request):
    logout(request)
    return render(request,"index.html")

def shop_logout(request):
    return render(request,"index.html")
