from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import *
# Create your views here.

def homepage(request):

    if request.user.is_authenticated:
        profile = userProfile.objects.filter(user = request.user).first()
        products_shop = Product.objects.filter(Q(user = request.user) & Q(approved = True) & Q(sell = False))
        all_chats_to = []
        #  all_chats_to = []
        chats = Chat.objects.filter(to_user = request.user)
        for chat in chats:
            all_chats_to.append({"username":chat.from_user,"image":"pro.image.url","message":"mesg.message"})

        chats2 = Chat.objects.filter(from_user = request.user)
        for chat in chats2:
            all_chats_to.append({"username":chat.to_user,"image":"pro.image.url","message":"mesg.message"})

            # all_chats_to.append({"username":chat.to_user,"image":pro.image.url,"message":"mesg.message"})
    else:
        profile = ''
        products_shop = []
        all_chats_to = []

    comments = Comment.objects.all()
    
    doctors = userProfile.objects.filter(added_by = request.user.username)
    doctors_list = []
    for doc in doctors:

        app = Appointment.objects.filter(Q(username = request.user.username) & Q(doctor = doc.user.username) & Q(done = False)).first()
        if app:
            doctors_list.append({"user":doc.user,"image":doc.image,"first_name":doc.user.first_name,"last_name":doc.user.last_name,"address":doc.address,"phone":doc.phone,"specialization":doc.specialization,"booked":True})
        else:
            doctors_list.append({"user":doc.user,"image":doc.image,"first_name":doc.user.first_name,"last_name":doc.user.last_name,"address":doc.address,"phone":doc.phone,"specialization":doc.specialization,"booked":False})

    doctors_all = userProfile.objects.filter(is_doctor = True)
    doctors_list_2 = []
    from datetime import date
    for doc in doctors_all:
        times = Time.objects.filter(username = doc.user.username)
        time_final = []
        for time in times:
            today = date.today()

            app = Appointment.objects.filter(Q(date = today) & Q(doctor = doc.user.username) & Q(done = False) & Q(time = time.time)).first()
            # print(app +"---------")
            try:
                if not app.date == today:
                    # time_final.append(time.time)
                    print(time.time)
                else:
                    time_final.append(time.time)
            except:
                time_final.append(time.time)

        app = Appointment.objects.filter(Q(username = request.user.username) & Q(doctor = doc.user.username) & Q(done = False)).first()
        if app:

            doctors_list_2.append({"user":doc.user,"image":doc.image,"first_name":doc.user.first_name,"last_name":doc.user.last_name,"address":doc.address,"phone":doc.phone,"specialization":doc.specialization,"booked":True,"time":time_final,"added_by":doc.added_by,"district":doc.district})
        else:
            doctors_list_2.append({"user":doc.user,"image":doc.image,"first_name":doc.user.first_name,"last_name":doc.user.last_name,"address":doc.address,"phone":doc.phone,"specialization":doc.specialization,"booked":False,"time":time_final,"added_by":doc.added_by,"district":doc.district})
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user = request.user).order_by('-date')
    else:
        notifications = []
    appointments = Appointment.objects.filter(doctor = request.user.username)

    return render(request,'index.html',context = {'profile':profile,"products":[],"products_shop":products_shop[:4],'chats':all_chats_to,"comments":comments,"doctors":doctors_list,"appointments":appointments,"doctors2":doctors_list_2,"notifications":notifications,"userapps":Appointment.objects.filter(username  = request.user.username),"blogs":Blog.objects.all()})


def leave(request):
    Leave.objects.create(date = request.POST.get('date'),username = request.user.username)
    return HttpResponseRedirect(reverse('homepage'))

def editsymp(request,pk):

    appointments = Appointment.objects.filter(pk = pk).first()
    appointments.symptoms = request.POST.get('text')
    appointments.save()

    return HttpResponseRedirect(reverse('homepage'))

def appsall(request):

    if request.user.is_authenticated:
        profile = userProfile.objects.filter(user = request.user).first()
        products_shop = Product.objects.filter(Q(user = request.user) & Q(approved = True) & Q(sell = False))
        all_chats_to = []
        #  all_chats_to = []
        chats = Chat.objects.filter(to_user = request.user)
        for chat in chats:
            all_chats_to.append({"username":chat.from_user,"image":"pro.image.url","message":"mesg.message"})

        chats2 = Chat.objects.filter(from_user = request.user)
        for chat in chats2:
            all_chats_to.append({"username":chat.to_user,"image":"pro.image.url","message":"mesg.message"})

            # all_chats_to.append({"username":chat.to_user,"image":pro.image.url,"message":"mesg.message"})
    else:
        profile = ''
        products_shop = []
        all_chats_to = []

    comments = Comment.objects.all()
    products = Product.objects.all()

    products_list = []
    try:

        for product in products:
            car = cart.objects.filter(Q(product = product) & Q(user = request.user)).first()
            if car:
                products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":True,"user":product.user})
            else:
                products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":False,"user":product.user})
    except:
        products_list = products
    doctors = userProfile.objects.filter(added_by = request.user.username)
    doctors_list = []
    for doc in doctors:

        app = Appointment.objects.filter(Q(username = request.user.username) & Q(doctor = doc.user.username) & Q(done = False)).first()
        if app:
            doctors_list.append({"user":doc.user,"image":doc.image,"first_name":doc.user.first_name,"last_name":doc.user.last_name,"address":doc.address,"phone":doc.phone,"specialization":doc.specialization,"booked":True})
        else:
            doctors_list.append({"user":doc.user,"image":doc.image,"first_name":doc.user.first_name,"last_name":doc.user.last_name,"address":doc.address,"phone":doc.phone,"specialization":doc.specialization,"booked":False})

    doctors_all = userProfile.objects.filter(is_doctor = True)
    doctors_list_2 = []
    from datetime import date
    for doc in doctors_all:
        times = Time.objects.filter(username = doc.user.username)
        time_final = []
        for time in times:
            today = date.today()

            app = Appointment.objects.filter(Q(date = today) & Q(doctor = doc.user.username) & Q(done = False) & Q(time = time.time)).first()
            # print(app +"---------")
            try:
                if not app.date == today:
                    # time_final.append(time.time)
                    print(time.time)
                else:
                    time_final.append(time.time)
            except:
                time_final.append(time.time)

        app = Appointment.objects.filter(Q(username = request.user.username) & Q(doctor = doc.user.username) & Q(done = False)).first()
        if app:

            doctors_list_2.append({"user":doc.user,"image":doc.image,"first_name":doc.user.first_name,"last_name":doc.user.last_name,"address":doc.address,"phone":doc.phone,"specialization":doc.specialization,"booked":True,"time":time_final,"added_by":doc.added_by,"district":doc.district})
        else:
            doctors_list_2.append({"user":doc.user,"image":doc.image,"first_name":doc.user.first_name,"last_name":doc.user.last_name,"address":doc.address,"phone":doc.phone,"specialization":doc.specialization,"booked":False,"time":time_final,"added_by":doc.added_by,"district":doc.district})
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user = request.user).order_by('-date')
    else:
        notifications = []
    appointments = Appointment.objects.filter(doctor = request.user.username)

    return render(request,'appointments.html',context = {'profile':profile,"products":products_list[:4],"products_shop":products_shop[:4],'chats':all_chats_to,"comments":comments,"doctors":doctors_list,"appointments":appointments,"doctors2":doctors_list_2,"notifications":notifications,"userapps":Appointment.objects.filter(username  = request.user.username)})

def therapists(request):

    if request.user.is_authenticated:
        profile = userProfile.objects.filter(user = request.user).first()
        products_shop = Product.objects.filter(Q(user = request.user) & Q(approved = True) & Q(sell = False))
        all_chats_to = []
        #  all_chats_to = []
        chats = Chat.objects.filter(to_user = request.user)
        for chat in chats:
            all_chats_to.append({"username":chat.from_user,"image":"pro.image.url","message":"mesg.message"})

        chats2 = Chat.objects.filter(from_user = request.user)
        for chat in chats2:
            all_chats_to.append({"username":chat.to_user,"image":"pro.image.url","message":"mesg.message"})

            # all_chats_to.append({"username":chat.to_user,"image":pro.image.url,"message":"mesg.message"})
    else:
        profile = ''
        products_shop = []
        all_chats_to = []

    comments = Comment.objects.all()
    products = Product.objects.all()

    products_list = []
    try:

        for product in products:
            car = cart.objects.filter(Q(product = product) & Q(user = request.user)).first()
            if car:
                products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":True,"user":product.user})
            else:
                products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":False,"user":product.user})
    except:
        products_list = products
    doctors = userProfile.objects.filter(added_by = request.user.username)
    doctors_list = []
    for doc in doctors:

        app = Appointment.objects.filter(Q(username = request.user.username) & Q(doctor = doc.user.username) & Q(done = False)).first()
        if app:
            doctors_list.append({"user":doc.user,"image":doc.image,"first_name":doc.user.first_name,"last_name":doc.user.last_name,"address":doc.address,"phone":doc.phone,"specialization":doc.specialization,"booked":True})
        else:
            doctors_list.append({"user":doc.user,"image":doc.image,"first_name":doc.user.first_name,"last_name":doc.user.last_name,"address":doc.address,"phone":doc.phone,"specialization":doc.specialization,"booked":False})

    doctors_all = Doctor.objects.filter(is_doctor = False)
    doctors_list_2 = []
    from datetime import date
    for doc in doctors_all:
        doc = userProfile.objects.filter(user = doc.user).first()
        leaves = Leave.objects.filter(username = doc.user.username)
        times = Time.objects.filter(username = doc.user.username)
        time_final = []
        leaves_all  = []
        for time in times:
            today = date.today()

            app = Appointment.objects.filter(Q(date = today) & Q(doctor = doc.user.username) & Q(done = False) & Q(time = time.time)).first()
            # print(app +"---------")
            try:
                if not app.date == today:
                    # time_final.append(time.time)
                    print(time.time)
                else:
                    time_final.append(time.time)
            except:
                time_final.append(time.time)
        
        for leave in leaves:
            try:
                leaves_all.append(leave.date)
            except:
                pass


        app = Appointment.objects.filter(Q(username = request.user.username) & Q(doctor = doc.user.username) & Q(done = False)).first()
        if app:

            doctors_list_2.append({"leaves":leaves_all,"user":doc.user,"image":doc.image,"first_name":doc.user.first_name,"last_name":doc.user.last_name,"address":doc.address,"phone":doc.phone,"specialization":doc.specialization,"booked":True,"time":time_final,"added_by":doc.added_by,"district":doc.district,'reject':doc.reject,"is_doctor":doc.is_doctor})
        else:
            doctors_list_2.append({"leaves":leaves_all,"user":doc.user,"image":doc.image,"first_name":doc.user.first_name,"last_name":doc.user.last_name,"address":doc.address,"phone":doc.phone,"specialization":doc.specialization,"booked":False,"time":time_final,"added_by":doc.added_by,"district":doc.district,'reject':doc.reject,"is_doctor":doc.is_doctor})
        
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user = request.user).order_by('-date')
    else:
        notifications = []
    appointments = Appointment.objects.filter(doctor = request.user.username)

    return render(request,'therapist.html',context = {'profile':profile,"products":products_list[:4],"products_shop":products_shop[:4],'chats':all_chats_to,"comments":comments,"doctors":doctors_list,"appointments":appointments,"doctors2":doctors_list_2,"notifications":notifications,"userapps":Appointment.objects.filter(username  = request.user.username)})


message = 0
reg_error = 0

def checkSignup(request):

    username = request.POST.get('username')
    password = request.POST.get('password')


    u = User.objects.filter(username = username).first()

    if u == None:
        message = 0
    else:
        message = 1

    return JsonResponse({"message":message})

from django.core.files.storage import FileSystemStorage

def register(request):
    file = request.FILES.get('image')
    # fss = FileSystemStorage()
    # filename = fss.save(file.name,file)
    # url = fss.url(filename)

    if request.method == 'POST':
        try:
            user = User.objects.create(username = request.POST.get('username'),email=request.POST.get('email'))
            user.set_password(request.POST.get('password'))
            user.save()

        except:
            pass

        user = User.objects.filter(username=request.POST.get('username')).first()

        profile = userProfile.objects.create(user=user)
        profile.phone = request.POST.get('phone')
        profile.image = file
        profile.address = request.POST.get('address')
        # Chat.objects.create(from_user = request.POST.get('username'),to_user = "Therapist")

        profile.save()



    return HttpResponseRedirect(reverse('homepage'))

def registerShop(request):

    file = request.FILES.get('image')
    fss = FileSystemStorage()
    filename = fss.save(file.name,file)
    url = fss.url(filename)
    if request.method == 'POST':
        try:
            user = User.objects.create(username = request.POST.get('username'),email=request.POST.get('email'))
            user.set_password(request.POST.get('password'))
            user.save()
        except:
            pass

        user = User.objects.filter(username=request.POST.get('username')).first()

        profile = userProfile.objects.create(user=user)
        profile.shopkeeperPhone = request.POST.get('phone')
        profile.shopkeeperAddress = request.POST.get('address')
        profile.shopkeeperName = request.POST.get('username')
        profile.shopType = request.POST.get('type')
        profile.shopkeeperLocation = ""
        profile.image = file
        profile.accountType = "ShopKeeper"
        profile.save()
        ShopKeeper.objects.create(shopkeeperName = request.POST.get('username'),shopkeeperPhone = request.POST.get('phone'),email =request.POST.get('email'),shopkeeperAddress = request.POST.get('address'),shopType = request.POST.get('type'),user = user)


    return HttpResponseRedirect(reverse('homepage'))


def registerHosp(request):

    file = request.FILES.get('image')
    fss = FileSystemStorage()
    filename = fss.save(file.name,file)
    url = fss.url(filename)
    if request.method == 'POST':
        try:
            user = User.objects.create(username = request.POST.get('username'),email=request.POST.get('email'))
            user.set_password(request.POST.get('password'))
            user.save()
        except:
            pass

        user = User.objects.filter(username=request.POST.get('username')).first()

        profile = userProfile.objects.create(user=user)
        profile.hospitalPhone = request.POST.get('phone')
        profile.hospitalAddress = request.POST.get('address')
        profile.hospitalName = request.POST.get('username')
        profile.hospitalType = request.POST.get('type')
        profile.shopkeeperLocation = ""
        profile.image = file
        profile.accountType = "Hospital"
        profile.save()
        Hospital.objects.create(hospitalName = request.POST.get('username'),hospitalPhone = request.POST.get('phone'),email =request.POST.get('email'),hospitalAddress = request.POST.get('address'),user = user)


    return HttpResponseRedirect(reverse('homepage'))


def registerDoc(request):

    file = request.FILES.get('image')
    fss = FileSystemStorage()
    filename = fss.save(file.name,file)
    url = fss.url(filename)
    if request.method == 'POST':
        try:
            user = User.objects.create(username = request.POST.get('username'),email=request.POST.get('email'),first_name = request.POST.get('firstname'),last_name = request.POST.get('lastname'))
            user.set_password(request.POST.get('password'))
            user.save()
        except:
            pass

        user = User.objects.filter(username=request.POST.get('username')).first()

        profile = userProfile.objects.create(user=user)
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')

        profile.specialization = request.POST.get('type')
        profile.is_doctor = True
        profile.added_by = ""
        profile.district = request.POST.get('city')
        profile.image = file
        profile.save()
    time = request.POST.get("time")
    time_list = time.split(',')
    for time in time_list:
        Time.objects.create(username = request.POST.get('username'),time = time)
        print(time + " added")
    Doctor.objects.create(Name = request.POST.get('username'),phone = request.POST.get('phone'),email =request.POST.get('email'),address = request.POST.get('address'),user = user,specialization = request.POST.get('type'))

    return HttpResponseRedirect(reverse('homepage'))

def checkLogin1(request):

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username = username,password = password)
    if user:
        print(username)
        return JsonResponse({"message":0})

    else:
        print("No user found")
        return JsonResponse({"message":1})


def user_login1(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username,password = password)
        if user:

            if user.is_active:
                login(request, user)
                print("login success!!!")
                return HttpResponseRedirect(reverse('homepage'))
        else:

            print("No such user")


    return HttpResponseRedirect(reverse('homepage'))

@login_required
def user_logout(request):

    logout(request)


    return HttpResponseRedirect(reverse('homepage'))

def show_login(request):
    return render(request,'login.html')

def show_register(request):
    return render(request,'register.html')
def create_blog(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        desc = request.POST.get('desc')


        Blog.objects.create(name=name, image=image, desc=desc)
    return HttpResponseRedirect(reverse('homepage'))

def addProduct(request):

    profile = userProfile.objects.filter(user = request.user).first()
    if not profile.shopType == "Book" and not profile.shopType == "Device":
        product = Product.objects.create(user = request.user,
                                        image = request.FILES['image'],
                                        userImage = profile.image.url,
                                        name =  request.POST.get('name'),
                                        stock = request.POST.get('dosage'),
                                        price = request.POST.get('price'),
                                        route = request.POST.get('route'),
                                        activeIngredient = request.POST.get('activeIngredient'),
                                        manufacturerName  = profile.user.username,
                                        manufacturerAddress = profile.shopkeeperAddress,
                                        manufacturerCountry = profile.shopkeeperLocation,
                                        manufacturerContactNumber = profile.shopkeeperPhone,
                                        productType = profile.shopType
                                        )
    else:
        product = Product.objects.create(user = request.user,
                                        image = request.FILES['image'],
                                        userImage = profile.image.url,
                                        name =  request.POST.get('name'),
                                        stock = request.POST.get('dosage'),
                                        price = request.POST.get('price'),


                                        manufacturerName  = profile.user.username,
                                        manufacturerAddress = profile.shopkeeperAddress,
                                        manufacturerCountry = profile.shopkeeperLocation,
                                        manufacturerContactNumber = profile.shopkeeperPhone,
                                        productType = profile.shopType
                                        )



    return HttpResponseRedirect(reverse('homepage'))

def productView(request,pk):

    profile = userProfile.objects.filter(user = request.user).first()
    product = Product.objects.filter(pk = pk).first()
    ct = cart.objects.filter(user = request.user,product = product).first()

    products = Product.objects.filter(user = product.user)

    return render(request,'productView.html',{"product":product,"profile":profile,"cart":ct,"products":products,"name":product.name})



def status(request,pk):



    return HttpResponseRedirect(reverse('homepage'))

def addToCart(request):
    product = Product.objects.filter(pk = request.POST.get('pk')).first()
    price = product.price
    total = 0

    if product.stock >= int(request.POST.get('quantity')):
        out = 0
    else:
        out = 1
    if out == 0:
        for i in range(0,int(request.POST.get('quantity'))):
            total = total + price
        print("heyyy")
        ct = cart.objects.create(user = request.user,product = product,quantity = request.POST.get('quantity'),price = total)
    return JsonResponse({"success":1,"out":out})


def carts(request):
    profile = userProfile.objects.filter(user = request.user).first()
    ct = cart.objects.filter(user = request.user)
    products = []

    for c in ct:


        products.append({"name":c.product.name,"price":c.price,"quantity":c.quantity,"image":c.product.image,"pk":c.pk})

    print(products)
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user = request.user).order_by('-date')
    else:
        notifications = []
    appointments = Appointment.objects.filter(Q(doctor = request.user.username) & Q(done = False))
    return render(request,'cart.html',{"cart":products,"profile":profile,"carts":ct,"notifications":notifications})



def shop(request):

    if request.user.is_authenticated:
        profile = userProfile.objects.filter(user = request.user).first()
        products_shop = Product.objects.filter(Q(user = request.user) & Q(approved = True) & Q(sell = False))
    else:
        profile = ''
        products_shop = Product.objects.all()

    products_herb = userProfile.objects.filter(shopType = "Medicine")
    products_veg = userProfile.objects.filter(shopType = "Book")
    products_fruit = userProfile.objects.filter(shopType = "Device")
    products_list = []
    products_list_veg = []
    products_list_fruit = []
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user = request.user).order_by('-date')
    else:
        notifications = []
    # for product in products_herb:
    #     car = cart.objects.filter(Q(product = product) & Q(user = request.user)).first()
    #     if car:
    #         products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":True})
    #     else:
    #         products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":False})

    # for product in products_veg:
    #     car = cart.objects.filter(Q(product = product) & Q(user = request.user)).first()
    #     if car:
    #         products_list_veg.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":True})
    #     else:
    #         products_list_veg.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":False})

    # for product in products_fruit:
    #     car = cart.objects.filter(Q(product = product) & Q(user = request.user)).first()
    #     if car:
    #         products_list_fruit.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":True})
    #     else:
    #         products_list_fruit.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":False})

    return render(request,'shop.html',context = {'profile':profile,"products":products_herb,"products_shop":products_shop,"fruits":products_fruit,"veg":products_veg,"notifications":notifications})




def buy(request):
    from_user = userProfile.objects.filter(user = request.user).first()
    product = Product.objects.filter(pk = request.POST.get('pk')).first()
    # print("Quantity",request.POST.get('quantity'))
    if from_user.balance - int(request.POST.get('price')) > 0 and product.stock >= int(request.POST.get('quantity')):
        success = 1
    else:
        success = 0
    print(success)
    if product.stock >= int(request.POST.get('quantity')):
        if from_user.balance - int(request.POST.get('price')) > 0:
            to = userProfile.objects.filter(user = product.user).first()
            to.balance = to.balance + int(request.POST.get('price'))
            from_user.balance = from_user.balance - int(request.POST.get('price'))
            to.save()
            from_user.save()
            success = 1
            product.stock = product.stock - int(request.POST.get('quantity'))
            product.save()
            Notification.objects.create(user = request.user,message = "Your order of " + product.name + " has been placed and will be delivered to you soon.",product_pk = product.pk)
            Payment.objects.create(from_user = request.user.username,to_user = product.user.username ,amount = request.POST.get('price'),product = product.name)
            Notification.objects.create(user = product.user,message = "Order of " + product.name + " has been placed by " + request.user.username,product_pk = product.pk)

        else:
            success = 0
        out = 0

    else:
        out = 1


    order = Order.objects.create(user = request.user,product = product,address = from_user.address,quantity = request.POST.get('quantity'),price = request.POST.get('price'),to = product.user.username)

    return JsonResponse({"success":success,"out":out})


def buyAdd(request):
    from_user = userProfile.objects.filter(user = request.user).first()
    product = Product.objects.filter(pk = request.POST.get('pk')).first()
    # print("Quantity",request.POST.get('quantity'))

    if product.stock >= int(request.POST.get('quantity')):
        out = 0
        order = Order.objects.create(user = request.user,product = product,address = from_user.address,quantity = request.POST.get('quantity'),price = request.POST.get('price'),to = product.user.username)
        product.stock = product.stock - int(request.POST.get('quantity'))
        product.save()
        Notification.objects.create(user = request.user,message = "Your order of " + product.name + " has been placed and will be delivered to you soon.",product_pk = product.pk)
        Notification.objects.create(user = product.user,message = "Order of " + product.name + " has been placed by " + request.user.username,product_pk = product.pk)


    else:
        out = 1

    print("Successfully placed order",from_user.address)
    return JsonResponse({"success":1,"out":out})

def buyAll(request):
    ct = cart.objects.filter(user = request.user)
    total = 0
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    for prod in ct:
        total = 0
        total = total + prod.price

        from_user = userProfile.objects.filter(user = request.user).first()
        product = Product.objects.filter(pk = prod.product.pk).first()
        quantity = product
        if from_user.balance - total > 0:
            to = userProfile.objects.filter(user = product.user).first()
            to.balance = to.balance + total
            from_user.balance = from_user.balance - total
            to.save()
            from_user.save()
            success = 1
            order = Order.objects.create(user = request.user,product = prod.product,address = from_user.address,quantity = prod.quantity,price = prod.price,to = product.user.username)
            print("----------------------------")
            Notification.objects.create(user = request.user,message = "Your order of " +prod.product.name + " has been placed and will be delivered to you soon.",product_pk = prod.product.pk)
            Notification.objects.create(user = prod.user,message = "Order of " + prod.product.name + " has been placed by " + request.user.username,product_pk = prod.product.pk)

            ct = cart.objects.filter(user = request.user,product = prod.product)
            ct.delete()
        else:
            success = 0
            break


    return JsonResponse({"success":success})

def buy2(request):
    from_user = userProfile.objects.filter(user = request.user).first()
    product = Product.objects.filter(pk = request.POST.get('pk')).first()
    if from_user.balance - int(request.POST.get('price')) > 0:
        to = userProfile.objects.filter(user = product.user).first()
        to.balance = to.balance + int(request.POST.get('price'))
        from_user.balance = from_user.balance - int(request.POST.get('price'))
        to.save()
        from_user.save()
        success = 1
    else:
        success = 0

    try:
        ct = cart.objects.filter(user = request.user,product = product)
        ct.delete()
    except:
        pass

    order = Order.objects.create(user = request.user,product = product,address = from_user.address,quantity = request.POST.get('quantity'),price = request.POST.get('price'),to = product.user.username)
    Notification.objects.create(user = product.user,message = "Order of " + product.name + " has been placed by " + request.user.username,product_pk = prod.product.pk)

    return JsonResponse({"success":success})


def orders(request):


    profile = userProfile.objects.filter(user = request.user).first()



    print(profile.is_shopkeeper)
    if not profile.is_shopkeeper:
        orders_all = Order.objects.filter(user = request.user)

    else:
        orders_all = Order.objects.filter(to = request.user.username)
    print(orders_all)
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user = request.user).order_by('-date')
    else:
        notifications = []
    return render(request,'orders.html',context = {'profile':profile,"orders":orders_all,"notifications":notifications})

def search(request):

    if request.user.is_authenticated:
        profile = userProfile.objects.filter(user = request.user).first()

    else:
        profile = ''

    orders_all = Product.objects.filter(name__icontains = request.POST.get('query'))

    print(orders_all)
    return render(request,'search.html',context = {'profile':profile,"products":orders_all})

def delete(request,pk):

    product = Product.objects.filter(pk = pk).first()
    product.delete()
    return HttpResponseRedirect(reverse('homepage'))




import os
import openai

openai.api_key = "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"

def sendMsg1(request):

    chat = Chat.objects.filter(Q(from_user = request.POST.get('from_user')) & Q(to_user = request.POST.get('to_user'))).first()

    if chat:
        # chatObj = Chat.objects.create(from_user = request.POST.get('from_user') ,to_user = request.POST.get('to_user'))
        message = Message.objects.create(chat = chat,message = request.POST.get("message"),user = request.POST.get('from_user'))
    else:
        chat = Chat.objects.filter(Q(from_user = request.POST.get('to_user')) & Q(to_user = request.POST.get('from_user'))).first()
        if chat.from_user == request.user.username:
            message = Message.objects.create(chat = chat,message = request.POST.get("message"),user = chat.from_user)
        else:
            message = Message.objects.create(chat = chat,message = request.POST.get("message"),user = chat.to_user)


    return JsonResponse({"result":0})

def showMessages(request):


    chat = Chat.objects.filter(Q(from_user = request.POST.get('from_user')) & Q(to_user = request.POST.get("to_user"))).first()

    if chat:
        chat = Chat.objects.filter(Q(from_user = request.POST.get('from_user')) & Q(to_user = request.POST.get("to_user"))).first()

    else:
        chat = Chat.objects.filter(Q(from_user = request.POST.get('to_user')) & Q(to_user = request.POST.get("from_user"))).first()

    user = User.objects.filter(username = request.POST.get('to_user')).first()
    profile = userProfile.objects.filter(user = user).first()
    print(profile)
    messages = Message.objects.filter(chat = chat).all()

    msg_list = []
    for message in messages:

        m = {"from_user":message.user,"to_user": chat.to_user if chat.from_user != request.user.username else chat.to_user ,"message":message.message}


        msg_list.append(m)


    return JsonResponse({"message":msg_list,"image":profile.image.url})

def comment(request):

    Comment.objects.create(user = request.user,image = userProfile.objects.filter(user = request.user).first().image.url,comment = request.POST.get('comment'))

    return HttpResponseRedirect(reverse('homepage'))


def stock(request):

    product = Product.objects.filter(pk = request.POST.get('pk')).first()
    # print("Quantity",request.POST.get('quantity'))

    product.stock = int(request.POST.get('stock'))
    product.save()

    return JsonResponse({"stock":product.stock,"out":1})


def sell(request):

    product = Product.objects.filter(pk = request.POST.get('pk')).first()
    profile = userProfile.objects.filter(user = product.user).first()
    print(profile.shopkeeperAddress)
    sell = Product.objects.create(user = product.user,
                                     image = request.FILES['image'],
                                     userImage = profile.image.url,
                                     name =  request.POST.get('name'),

                                        stock = request.POST.get('stock'),
                                        manufacturerName  = profile.user.username,
                                        manufacturerAddress = profile.shopkeeperAddress,
                                        productType = profile.shopType,
                                        sell = True,
                                        approved = False ,
                                        manufacturerContactNumber = profile.shopkeeperPhone,
                                        manufacturerCountry = "Kerala",
                                        added_by = request.user.username,
                                        activeIngredient = request.POST.get('origin')
                                     )

    return productView(request,request.POST.get('pk'))


def notifications(request):


    profile = userProfile.objects.filter(user = request.user).first()
    products_list = Product.objects.filter(Q(user = request.user) & Q(sell = True) & Q(approved = False) & Q(banned = False))


    return render(request,'notifications.html',context = {'profile':profile,"products":products_list})


def approve(request):

    product = Product.objects.filter(pk = request.POST.get('pk')).first()
    product.price = request.POST.get('price')
    product.sell = False
    product.approved = True
    product.save()
    us = User.objects.filter(username = product.added_by).first()
    to = userProfile.objects.filter(user = us).first()
    from_user = userProfile.objects.filter(user = request.user).first()
    to.balance = to.balance + int(request.POST.get('price'))
    from_user.balance = from_user.balance - int(request.POST.get('price'))
    to.save()
    from_user.save()
    print(request.POST.get('price'))
    return HttpResponseRedirect(reverse('notifications'))


def reject(request,pk):

    product = Product.objects.filter(pk = pk).first()

    product.sell = True
    product.approved = False
    product.banned = True
    product.save()

    return HttpResponseRedirect(reverse('notifications'))


def cartView(request,pk):

    profile = userProfile.objects.filter(user = request.user).first()
    ct = cart.objects.filter(pk = pk).first()
    product = Product.objects.filter(pk = ct.product.pk).first()
    print(product)
    ct = cart.objects.filter(user = request.user,product = product).first()

    products = Product.objects.filter(Q(user = product.user) & Q(approved = True))
    #----------------------------------------------------------------
    return render(request,'viewCart.html',{"product":product,"profile":profile,"cart":ct,"products":products,"name":product.name})

def approvedoc(request,pk):

    us = User.objects.filter(pk=pk).first()
    profile = userProfile.objects.filter(user=us).first()
    profile.is_doctor = True 
    profile.save()

    #----------------------------------------------------------------
    return HttpResponseRedirect(reverse('therapists'))

def rejectdoc(request,pk):

    us = User.objects.filter(pk=pk).first()
    profile = userProfile.objects.filter(user=us).first()
    profile.is_doctor = False 
    profile.reject = True 
    profile.save()

    #----------------------------------------------------------------
    return HttpResponseRedirect(reverse('therapists'))

def music(request):

    if request.user.is_authenticated:
        profile = userProfile.objects.filter(user = request.user).first()
        products_shop = Product.objects.filter(Q(user = request.user) & Q(approved = True) & Q(sell = False))
        all_chats_to = []
        chats = Chat.objects.filter(to_user = request.user)

        for chat in chats:
            pro = userProfile.objects.filter(user = User.objects.filter(username = chat.from_user).first()).first()
            all_chats_to.append({"username":chat.from_user,"image":pro.image.url,"message":"mesg.message"})

        chats2 = Chat.objects.filter(from_user = request.user)
        for chat in chats2:
            pro = userProfile.objects.filter(user = User.objects.filter(username = chat.to_user).first()).first()

            all_chats_to.append({"username":chat.to_user,"image":pro.image.url,"message":"mesg.message"})
    else:
        profile = ''
        products_shop = []
        all_chats_to = []

    comments = Comment.objects.all()
    products = Product.objects.filter(Q(approved = True) & Q(sell = False))

    products_list = []
    try:

        for product in products:
            car = cart.objects.filter(Q(product = product) & Q(user = request.user)).first()
            if car:
                products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":True})
            else:
                products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":False})
    except:
        products_list = products
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user = request.user).order_by('-date')
    else:
        notifications = []
    return render(request,'music.html',context = {'profile':profile,"products":products_list[:4],"products_shop":products_shop[:4],'chats':all_chats_to,"comments":comments,"musics":Music.objects.all(),"notifications":notifications})


def meditation(request):

    if request.user.is_authenticated:
        profile = userProfile.objects.filter(user = request.user).first()
        products_shop = Product.objects.filter(Q(user = request.user) & Q(approved = True) & Q(sell = False))
        all_chats_to = []
        chats = Chat.objects.filter(to_user = request.user)

        for chat in chats:
            pro = userProfile.objects.filter(user = User.objects.filter(username = chat.from_user).first()).first()
            all_chats_to.append({"username":chat.from_user,"image":pro.image.url,"message":"mesg.message"})

        chats2 = Chat.objects.filter(from_user = request.user)
        for chat in chats2:
            pro = userProfile.objects.filter(user = User.objects.filter(username = chat.to_user).first()).first()

            all_chats_to.append({"username":chat.to_user,"image":pro.image.url,"message":"mesg.message"})
    else:
        profile = ''
        products_shop = []
        all_chats_to = []

    comments = Comment.objects.all()
    products = Product.objects.filter(Q(approved = True) & Q(sell = False))

    products_list = []
    try:

        for product in products:
            car = cart.objects.filter(Q(product = product) & Q(user = request.user)).first()
            if car:
                products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":True})
            else:
                products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":False})
    except:
        products_list = products
    all_classes = []

    classes = YogaClass.objects.all()
    for cl in classes:
        enroll = Enrollment.objects.filter(Q(username = request.user.username) & Q(yoga = cl)).first()
        if enroll:
            all_classes.append({"name":cl.name,"description":cl.description,"image":cl.image,"pk":cl.pk,"enroll":True})
        else:
            all_classes.append({"name":cl.name,"description":cl.description,"image":cl.image,"pk":cl.pk,"enroll":False})

    return render(request,'meditation.html',context = {'profile':profile,"products":products_list[:4],"products_shop":products_shop[:4],'chats':all_chats_to,"comments":comments,"musics":Music.objects.all(),"videos":all_classes,"notifications":notifications})

def enroll(request):
    Enrollment.objects.create(username = request.user.username,yoga = YogaClass.objects.filter(pk = request.POST.get('pk')).first())
    return HttpResponseRedirect(reverse('yoga'))

def myclasses(request):

    if request.user.is_authenticated:
        profile = userProfile.objects.filter(user = request.user).first()
        products_shop = Product.objects.filter(Q(user = request.user) & Q(approved = True) & Q(sell = False))
        all_chats_to = []
        chats = Chat.objects.filter(to_user = request.user)

        for chat in chats:
            pro = userProfile.objects.filter(user = User.objects.filter(username = chat.from_user).first()).first()
            all_chats_to.append({"username":chat.from_user,"image":pro.image.url,"message":"mesg.message"})

        chats2 = Chat.objects.filter(from_user = request.user)
        for chat in chats2:
            pro = userProfile.objects.filter(user = User.objects.filter(username = chat.to_user).first()).first()

            all_chats_to.append({"username":chat.to_user,"image":pro.image.url,"message":"mesg.message"})
    else:
        profile = ''
        products_shop = []
        all_chats_to = []

    comments = Comment.objects.all()
    products = Product.objects.filter(Q(approved = True) & Q(sell = False))

    products_list = []
    try:

        for product in products:
            car = cart.objects.filter(Q(product = product) & Q(user = request.user)).first()
            if car:
                products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":True})
            else:
                products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":False})
    except:
        products_list = products
    all_classes = []

    classes = YogaClass.objects.all()
    for cl in classes:
        enroll = Enrollment.objects.filter(Q(username = request.user.username) & Q(yoga = cl)).first()
        if enroll:
            all_classes.append({"name":cl.name,"description":cl.description,"image":cl.image,"pk":cl.pk,"enroll":True})
        else:
            all_classes.append({"name":cl.name,"description":cl.description,"image":cl.image,"pk":cl.pk,"enroll":False})

    return render(request,'myclasses.html',context = {'profile':profile,"products":products_list[:4],"products_shop":products_shop[:4],'chats':all_chats_to,"comments":comments,"musics":Music.objects.all(),"videos":Enrollment.objects.filter(username = request.user.username),"notifications":notifications})


def viewClass(request,pk):

    if request.user.is_authenticated:
        profile = userProfile.objects.filter(user = request.user).first()
        products_shop = Product.objects.filter(Q(user = request.user) & Q(approved = True) & Q(sell = False))
        all_chats_to = []
        chats = Chat.objects.filter(to_user = request.user)

        for chat in chats:
            pro = userProfile.objects.filter(user = User.objects.filter(username = chat.from_user).first()).first()
            all_chats_to.append({"username":chat.from_user,"image":pro.image.url,"message":"mesg.message"})

        chats2 = Chat.objects.filter(from_user = request.user)
        for chat in chats2:
            pro = userProfile.objects.filter(user = User.objects.filter(username = chat.to_user).first()).first()

            all_chats_to.append({"username":chat.to_user,"image":pro.image.url,"message":"mesg.message"})
    else:
        profile = ''
        products_shop = []
        all_chats_to = []

    comments = Comment.objects.all()
    products = Product.objects.filter(Q(approved = True) & Q(sell = False))

    products_list = []
    try:

        for product in products:
            car = cart.objects.filter(Q(product = product) & Q(user = request.user)).first()
            if car:
                products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":True})
            else:
                products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":False})
    except:
        products_list = products
    all_classes = []

    classes = YogaClass.objects.all()
    for cl in classes:
        enroll = Enrollment.objects.filter(Q(username = request.user.username) & Q(yoga = cl)).first()
        if enroll:
            all_classes.append({"name":cl.name,"description":cl.description,"image":cl.image,"pk":cl.pk,"enroll":True})
        else:
            all_classes.append({"name":cl.name,"description":cl.description,"image":cl.image,"pk":cl.pk,"enroll":False})

    yogas = videoSolution.objects.filter(chapter = YogaClass.objects.filter(pk = pk).first())
    return render(request,'videos.html',context = {'profile':profile,"products":products_list[:4],"products_shop":products_shop[:4],'chats':all_chats_to,"comments":comments,"musics":Music.objects.all(),"videos":yogas,"notifications":notifications})


def depression(request):

    if request.user.is_authenticated:
        profile = userProfile.objects.filter(user = request.user).first()
        products_shop = Product.objects.filter(Q(user = request.user) & Q(approved = True) & Q(sell = False))
        all_chats_to = []
        chats = Chat.objects.filter(to_user = request.user)

        for chat in chats:
            pro = userProfile.objects.filter(user = User.objects.filter(username = chat.from_user).first()).first()
            all_chats_to.append({"username":chat.from_user,"image":pro.image.url,"message":"mesg.message"})

        chats2 = Chat.objects.filter(from_user = request.user)
        for chat in chats2:
            pro = userProfile.objects.filter(user = User.objects.filter(username = chat.to_user).first()).first()

            all_chats_to.append({"username":chat.to_user,"image":pro.image.url,"message":"mesg.message"})
    else:
        profile = ''
        products_shop = []
        all_chats_to = []

    comments = Comment.objects.all()
    products = Product.objects.filter(Q(approved = True) & Q(sell = False))

    products_list = []
    try:

        for product in products:
            car = cart.objects.filter(Q(product = product) & Q(user = request.user)).first()
            if car:
                products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":True})
            else:
                products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":False})
    except:
        products_list = products

    doctors_list_2 = []
    from datetime import date
    doctors_all = userProfile.objects.filter(is_doctor = True)
    for doc in doctors_all:
        times = Time.objects.filter(username = doc.user.username)
        time_final = []
        for time in times:
            today = date.today()
            app = Appointment.objects.filter(Q(date = today) & Q(doctor = doc.user.username) & Q(done = False) & Q(time = time.time)).first()
            # print(app +"---------")
            try:
                if not app.date == today:
                    # time_final.append(time.time)
                    print(time.time)
                else:
                    time_final.append(time.time)
            except:
                time_final.append(time.time)

        app = Appointment.objects.filter(Q(username = request.user.username) & Q(doctor = doc.user.username) & Q(done = False)).first()
        if app:

            doctors_list_2.append({"user":doc.user,"image":doc.image,"first_name":doc.user.first_name,"last_name":doc.user.last_name,"address":doc.address,"phone":doc.phone,"specialization":doc.specialization,"booked":True,"time":time_final,"added_by":doc.added_by})
        else:
            doctors_list_2.append({"user":doc.user,"image":doc.image,"first_name":doc.user.first_name,"last_name":doc.user.last_name,"address":doc.address,"phone":doc.phone,"specialization":doc.specialization,"booked":False,"time":time_final,"added_by":doc.added_by})
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user = request.user).order_by('-date')
    else:
        notifications = []
    appointments = Appointment.objects.filter(Q(doctor = request.user.username) & Q(done = False))

    return render(request,'depression.html',context = {'profile':profile,"products":products_list[:4],"products_shop":products_shop[:4],'chats':all_chats_to,"comments":comments,"musics":Music.objects.all(),"videos":videoSolution.objects.all(),"notifications":notifications,"doctors2":doctors_list_2})


import os
import openai

openai.api_key = "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"



def depressionCheck(request):


    text_data = request.POST.get('stringText')

    response = openai.Completion.create(
  model="text-davinci-003",
  prompt="determine if the given text is depressed or not just show if its depressed or not: "+text_data ,
  temperature=0.7,
  max_tokens=64,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)
    my_dict = {"result":str(response.choices[0].text).replace("\n\n","").replace("in this world","")}
    print(my_dict)
    return JsonResponse({"result":str(response.choices[0].text).replace("\n\n","").replace("in this world","")})


def blogs(request):

    if request.user.is_authenticated:
        profile = userProfile.objects.filter(user = request.user).first()
        products_shop = Product.objects.filter(Q(user = request.user) & Q(approved = True) & Q(sell = False))
        all_chats_to = []
        chats = Chat.objects.filter(to_user = request.user)

        for chat in chats:
            pro = userProfile.objects.filter(user = User.objects.filter(username = chat.from_user).first()).first()
            all_chats_to.append({"username":chat.from_user,"image":pro.image.url,"message":"mesg.message"})

        chats2 = Chat.objects.filter(from_user = request.user)
        for chat in chats2:
            pro = userProfile.objects.filter(user = User.objects.filter(username = chat.to_user).first()).first()

            all_chats_to.append({"username":chat.to_user,"image":pro.image.url,"message":"mesg.message"})
    else:
        profile = ''
        products_shop = []
        all_chats_to = []

    comments = Comment.objects.all()
    products = Product.objects.filter(Q(approved = True) & Q(sell = False))

    products_list = []
    try:

        for product in products:
            car = cart.objects.filter(Q(product = product) & Q(user = request.user)).first()
            if car:
                products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":True})
            else:
                products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":False})
    except:
        products_list = products
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user = request.user).order_by('-date')
    else:
        notifications = []
    return render(request,'blogs.html',context = {'profile':profile,"products":products_list[:4],"products_shop":products_shop[:4],'chats':all_chats_to,"comments":comments,"musics":Music.objects.all(),"videos":videoSolution.objects.all(),"blogs":Blog.objects.all(),"notifications":notifications})


def appointment(request):
    user = User.objects.filter(username = request.POST.get('doctor')).first()
    print(user)
    profile = userProfile.objects.filter(user = user).first()
    print(request.POST.get('doctor'))
    Appointment.objects.create(username = request.user.username,doctor = request.POST.get('doctor'),date = request.POST.get('date'),time = request.POST.get('time'),symptoms = request.POST.get('symptoms'),gender = request.POST.get('gender'),blood = request.POST.get('blood_group'))
    Notification.objects.create(user = request.user,message = "Dr. "+request.POST.get('doctor') + " appointment booked on " + request.POST.get('date') + " at " + request.POST.get('time'))
    user = User.objects.filter(username = profile.added_by).first()
    # Notification.objects.create(user = user,message = "Dr. "+request.POST.get('doctor') + " appointment booked on " + request.POST.get('date') + " at " + request.POST.get('time') + " by "+ request.user.username)

    return HttpResponseRedirect(reverse('homepage'))


def done(request):


    app = Appointment.objects.filter(pk = request.POST.get('pk')).first()
    app.done = True
    app.save()
    user = User.objects.filter(username = app.username).first()
    Notification.objects.create(user = user,message = "Dr. "+app.doctor + " appointment booked on " + app.date + " at " + app.time + " has been approved ")
    chat=Chat.objects.create(from_user = request.user.username,to_user = app.username)
    Message.objects.create(chat = chat,user = request.user.username,message = "Hii your appointment has been fixed on " + app.date + "at "+ app.time)


    return HttpResponseRedirect(reverse('homepage'))

def done1(request):


    app = Appointment.objects.filter(pk = request.POST.get('pk')).first()
    # app.done = True
    app.delete()
    user = User.objects.filter(username = app.username).first()
    Notification.objects.create(user = user,message = "Message to Dr. "+app.doctor + " has been stopped.Schedule an appointment to chat again" )
    chat=Chat.objects.filter(Q(from_user = request.user.username)&Q(to_user = app.username)).first()
    chat.delete()
    # Message.objects.create(chat = chat,user = request.user.username,message = "Hii your appointment has been fixed on " + app.date + "at "+ app.time)


    return HttpResponseRedirect(reverse('homepage'))

def prescription(request):

    app = Appointment.objects.filter(pk = request.POST.get('pk')).first()

    app.prescription =request.POST.get('prescription')
    app.save()

    user = User.objects.filter(username = app.username).first()
    Notification.objects.create(user = user,message = "Your prescription has been added by "+app.doctor )
    
    return HttpResponseRedirect(reverse('homepage'))


def rejectDoc(request):


    app = Appointment.objects.filter(pk = request.POST.get('pk')).first()
    app.reject = True
    app.delete()
    user = User.objects.filter(username = app.username).first()
    
    Notification.objects.create(user = user,message = "Dr. "+app.doctor + " appointment booked on " + app.date + " at " + app.time + " has been rejected ")


    return HttpResponseRedirect(reverse('homepage'))


def check(request):
    from_user = userProfile.objects.filter(user = request.user).first()
    product = Product.objects.filter(pk = request.POST.get('pk')).first()
    # print("Quantity",request.POST.get('quantity'))
    if from_user.balance - int(request.POST.get('price')) > 0 and product.stock >= int(request.POST.get('quantity')):
        success = 1
    else:
        success = 0
    print(success)
    if product.stock >= int(request.POST.get('quantity')):
        if from_user.balance - int(request.POST.get('price')) > 0:

            success = 1

        else:
            success = 0
        out = 0

    else:
        out = 1


    # order = Order.objects.create(user = request.user,product = product,address = from_user.address,quantity = request.POST.get('quantity'),price = request.POST.get('price'),to = product.user.username)

    return JsonResponse({"success":success,"out":out})


def cartDelete(request,pk):

    profile = userProfile.objects.filter(user = request.user).first()
    ct = cart.objects.filter(pk = pk).first()
    ct.delete()
    #----------------------------------------------------------------
    return HttpResponseRedirect(reverse('cart'))


def cancelOrder(request,pk):

    profile = userProfile.objects.filter(user = request.user).first()
    ct = Order.objects.filter(pk = pk).first()
    prod = Product.objects.filter(pk = ct.product.pk).first()
    print(prod)
    prod.stock = prod.stock + ct.quantity
    prod.save()
    noti = Notification.objects.filter(Q(user =  request.user) & Q(product_pk = prod.pk)).first()
    noti.delete()
    profile.balance = profile.balance + ct.price
    profile.save()
    to = userProfile.objects.filter(user = prod.user).first()
    to.balance = to.balance - ct.price
    to.save()
    ct.delete()

    return HttpResponseRedirect(reverse('orders'))



def shopView(request):

    if request.user.is_authenticated:
        profile = userProfile.objects.filter(user = request.user).first()
        products_shop = Product.objects.filter(Q(user = request.user) & Q(approved = True) & Q(sell = False))
        all_chats_to = []
        chats = Chat.objects.filter(to_user = request.user)

        for chat in chats:
            pro = userProfile.objects.filter(user = User.objects.filter(username = chat.from_user).first()).first()
            all_chats_to.append({"username":chat.from_user,"image":pro.image.url,"message":"mesg.message"})

        chats2 = Chat.objects.filter(from_user = request.user)
        for chat in chats2:
            pro = userProfile.objects.filter(user = User.objects.filter(username = chat.to_user).first()).first()

            all_chats_to.append({"username":chat.to_user,"image":pro.image.url,"message":"mesg.message"})
    else:
        profile = ''
        products_shop = []
        all_chats_to = []

    comments = Comment.objects.all()
    use = User.objects.filter(username = request.POST.get('name')).first()
    print(use)
    products = Product.objects.filter(user = use)

    products_list = []


    for product in products:
        car = cart.objects.filter(Q(product = product) & Q(user = request.user)).first()
        if car:
            products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":True,"user":product.user})
        else:
            products_list.append({"name":product.name,"price":product.price,"pk":product.pk,"image":product.image,"cart":False,"user":product.user})

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user = request.user).order_by('-date')
    else:
        notifications = []
    print(products_list)
    return render(request,'shopView.html',context = {'profile':profile,"products":products_list,"products_shop":products_shop[:4],'chats':all_chats_to,"comments":comments,"username":request.POST.get('name'),"notificaions":notifications})


def checkDate(request):
    from datetime import date
    date_req = request.POST.get('date')
    print(date_req,request.POST.get('username'))
    times = Time.objects.filter(username = request.POST.get('username'))
    time_final = []
    for time in times:
        today = date.today()
        app = Appointment.objects.filter(Q(date = date_req) & Q(doctor = request.POST.get('username')) & Q(done = False) & Q(time = time.time)).first()

        if not app:
            time_final.append(time.time)
        else:
            pass

    print(time_final)
    return JsonResponse({"message":message,"times":time_final})


def bill(request):
    profile = userProfile.objects.filter(user = request.user).first()
    ct = cart.objects.filter(user = request.user)
    products = []

    for c in ct:

        products.append(c.product)
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user = request.user)
    else:
        notifications = []
    total = 0
    for car in ct:
        total = total + car.price
    print(total)
    return render(request,'bill.html',{"cart":products,"profile":profile,"carts":ct,"notifications":notifications,"total":total,"count":cart.objects.filter(user = request.user).count()})

# def buyAll(request):
#     ct = cart.objects.filter(user = request.user)
#     products = []

#     for c in ct:
#         products.append(c.product)

#     from_user = userProfile.objects.filter(user = request.user).first()

#     total = 0
#     for car in ct:
#         total = total + car.price

#     from_user.balance = from_user.balance - total
#     from_user.save()

#     for c in ct:
#        c.product.stock = c.product.stock - c.quantity
#        c.product.save()
#        to_user = userProfile.objects.filter(user = c.product.user).first()
#        to_user.balance = to_user.balance + c.price
#        to_user.save()
#        Order.objects.create(user = request.user,product = c.product,address = from_user.address,quantity = c.quantity,price = c.price,to = c.product.user.username)
#        Notification.objects.create(user = request.user,message = "Your order of " + c.product.name + " has been placed and will be delivered to you soon.",product_pk = c.product.pk)
#        c.delete()
#     return JsonResponse({"success":1})


def checkAll(request):
    ct = cart.objects.filter(user = request.user)
    products = []

    for c in ct:
        products.append(c.product)

    from_user = userProfile.objects.filter(user = request.user).first()

    total = 0
    for car in ct:
        total = total + car.price

    if from_user.balance < total:
        success = 0
    else:
        success = 1
    message = ""
    out = 0
    for c in ct:
        if c.product.stock < c.quantity:
            message  = message + c.product.name + ", "
            out = 1
    print(message)
    # order = Order.objects.create(user = request.user,product = product,address = from_user.address,quantity = request.POST.get('quantity'),price = request.POST.get('price'),to = product.user.username)

    return JsonResponse({"success":success,"out":out,"message":message})



def cartDeleteAll(request,pk):

    profile = userProfile.objects.filter(user = request.user).first()
    ct = cart.objects.filter(pk = pk).first()
    ct.delete()
    #----------------------------------------------------------------
    return HttpResponseRedirect(reverse('bill'))


def buyAllAdd(request):
    ct = cart.objects.filter(user = request.user)
    products = []

    for c in ct:
        products.append(c.product)

    from_user = userProfile.objects.filter(user = request.user).first()

    total = 0
    for car in ct:
        total = total + car.price

    # from_user.balance = from_user.balance - total
    # from_user.save()
    for c in ct:
       c.product.stock = c.product.stock - c.quantity
       c.product.save()
       Order.objects.create(user = request.user,product = c.product,address = from_user.address,quantity = c.quantity,price = c.price,to = c.product.user.username)
       Notification.objects.create(user = request.user,message = "Your order of " + c.product.name + " has been placed and will be delivered to you soon.",product_pk = c.product.pk)
       c.delete()
    return JsonResponse({"success":1})



#For android application ---------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------



@csrf_exempt
def register1(request):
    data = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        try:
            user = User.objects.create(username = data['username'],email=data['email'])
            user.set_password(data['password'])
            user.save()

            user = User.objects.filter(username=data['username']).first()
            profile = userProfileApp.objects.create(user=user,registered_as = "User",phone = data["phone"],address = data["address"],specialization = "")

            dict = {'success': 'yes'}

            my_dict_json = json.dumps(dict)
        except:
            dict = {'success': 'no'}
            print("some error")

            my_dict_json = json.dumps(dict)

    return HttpResponse(my_dict_json, content_type='application/json')
@csrf_exempt
def registerDoctor(request):
    data = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        try:
            user = User.objects.create(username = data['username'],email=data['email'],first_name = data["fullname"])
            user.set_password(data['password'])
            user.save()

            user = User.objects.filter(username=data['username']).first()
            profile = userProfileApp.objects.create(user=user,registered_as = "Doctor",phone = data["phone"],address = data["address"],specialization = data["specialization"])

            dict = {'success': 'yes'}

            my_dict_json = json.dumps(dict)
        except:
            dict = {'success': 'no'}
            print("some error")

            my_dict_json = json.dumps(dict)

    return HttpResponse(my_dict_json, content_type='application/json')


def checkLogin(request):

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username = username,password = password)
    if user:
        print(username)
        return JsonResponse({"message":0})

    else:
        print("No user found")
        return JsonResponse({"message":1})

@csrf_exempt
def user_login(request):

    data = json.loads(request.body.decode('utf-8'))
    text_data = data['username']
    dt = []
    if request.method == 'POST':
        password = request.POST.get('password')
        print(data['username'])
        user = authenticate(username = data['username'],password = data['password'])
        if user:

            if user.is_active:
                login(request, user)
                print("login success!!!")
                # data = {"success":1}
                my_dict = {'success': 'yes'}
                my_dict_json = json.dumps(my_dict)

        else:
            data = {"success":1}
            print("No such user")
            my_dict = {'success': 'no'}
            my_dict_json = json.dumps(my_dict)

    return HttpResponse(my_dict_json, content_type='application/json')

@csrf_exempt
def user_logout(request):

    logout(request)
    print("logged out")

    return HttpResponseRedirect(reverse('homepage'))

import datetime
@csrf_exempt
def blogs(request):
    blogs = Blog.objects.all()
    data = []
    for blog in blogs:
        formatted_time = blog.date.strftime("%a %d %Y at %I:%M %p")
        product_data = {
            'name': blog.name,
            'pk':str(blog.pk),
            'desc':blog.desc,
            'image': request.build_absolute_uri(blog.image.url),
            'date' : formatted_time
        }
        print(request.build_absolute_uri(blog.image.url))
        data.append(product_data)
    return JsonResponse(data, safe=False)



import json
import re

def extract_floats(text):
    return re.findall(r'\d+\.\d+', text)


@csrf_exempt
def detect(request):

    data = json.loads(request.body.decode('utf-8'))

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",

        messages=[
            {"role": "system", "content": "You are a autism prediction bot. You will predict the likelihood of autism in an individual based on various factors. The inputs will be in the order of age, education level, family history, lifestyle, cognitive test scores, neuroimaging results,smoker,biomarker levels and other symptoms. Based on this, predict if the individual is likely to experience cognitive decline. Provide a probability score between 0 and 1.just give the probability value only nothing else"},
            {"role": "user", "content": str(data["age"])+","+data["education"]+","+data["family"]+","+data["lifestyle"] +","+str(data["score"]) +","+data["neuro"] +","+data["smoker"] +","+str(data["bio"]) +","+data["other"] },
        ]
        )
    data = []
    resmsg = response['choices'][0]['message']['content']
    floats = extract_floats(resmsg)

    print({"prob":str(float(floats[0]) * 100)})
    data.append({"prob":float(floats[0]) * 100})
    return JsonResponse(data, safe=False)


@csrf_exempt
def addComment(request):
    data = json.loads(request.body.decode('utf-8'))

    comment = Comment.objects.create(username = data['username'],comment=data['data'])
    print("Success");
    return JsonResponse("resmsg", safe=False)

@csrf_exempt
def comments(request):
    # data = json.loads(request.body.decode('utf-8'))

    comments_all = Comment.objects.all().order_by('-date')
    print(comments_all)
    data = []
    for comment in comments_all:
        comment_data = {
            'text': comment.comment,
            'date': comment.date,
            'username':comment.username
        }
        data.append(comment_data)
    return JsonResponse(data, safe=False)


def doctors(request):
    users = userProfile.objects.filter(is_doctor = True)
    data = []
    for user in users:
        print(user.user.first_name)
        user_dict = {
            'name': "Dr "+user.user.first_name,
            'username':user.user.username,
            'pk': str(user.user.pk),
            'email': user.user.email,
            'address': user.address,
            'phone': user.phone,
            # 'image': request.build_absolute_uri(user.image.url),
            'special':user.specialization
        }
        data.append(user_dict)
        print(data)
    return JsonResponse(data, safe=False)

@csrf_exempt
def classes(request):
    products = Activity.objects.all()
    data = []
    for product in products:
        formatted_time = product.date.strftime("%a %d %Y at %I:%M %p")
        product_data = {
            'name': product.name,
            'pk':str(product.pk),
            'description':product.desc,
            'image': request.build_absolute_uri(product.image.url),
            'date' : formatted_time,
            'link':product.link
        }
        print(request.build_absolute_uri(product.image.url))
        data.append(product_data)
    return JsonResponse(data, safe=False)



@csrf_exempt
def getChats(request):
    # print(request.POST.get('username'))


    chats = Chat.objects.filter(Q(from_user = request.POST.get('username')) | Q(to_user = request.POST.get('username'))).order_by('-date')
    username = request.POST.get('username')
    data = []

    for c in chats:
        if c.from_user != username:
            print(c.from_user)
            frmuser = User.objects.filter(username = c.from_user).first()
            frmprofile = userProfile.objects.filter(user = frmuser).first()
        else:
            frmuser = User.objects.filter(username = c.to_user).first()
            frmprofile = userProfile.objects.filter(user = frmuser).first()
        print(frmuser)
        message = Message.objects.filter(chat = c).order_by('-date').first()
        chat_data = {
            'name': c.from_user if username != c.from_user else c.to_user,
            'pk':str(c.pk),
            'message':message.message,

        }

        data.append(chat_data)

    return JsonResponse(data, safe=False)



@csrf_exempt
def messages(request):
    print(request.POST.get('username'))


    chat = Chat.objects.filter(Q( Q(from_user = request.POST.get('fromUser')) & Q(to_user = request.POST.get('toUser')) ) | Q(Q(from_user = request.POST.get('toUser')) & Q(to_user = request.POST.get('fromUser')))).first()

    username = request.POST.get('fromUser')
    data = []
    if chat:
        messagesAll = Message.objects.filter(chat = chat)
        for m in messagesAll:

            message = Message.objects.filter(chat = chat).order_by('-date').first()
            chat_data = {
                'name': m.user if username != m.user else username,

                'message':m.message,

            }

            data.append(chat_data)

    return JsonResponse(data, safe=False)
from django.utils import timezone
@csrf_exempt
def sendMsg(request):
    data = json.loads(request.body.decode('utf-8'))
    print(data['message'])
    msg = data['message']
    fromUser = data['fromUser']
    toUser = data['toUser']
    chat = Chat.objects.filter(Q( Q(from_user = data['fromUser']) & Q(to_user = data['toUser']) ) | Q(Q(from_user = data['toUser']) & Q(to_user = data['fromUser']))).first()

    # chat.date = timezone.now
    # chat.save()
    username = request.POST.get('fromUser')
    data = []
    if chat:
        Message.objects.create(chat = chat,user = fromUser,message = msg)
    else:
        ch = Chat.objects.create(from_user = fromUser ,to_user = toUser)
        Message.objects.create(message = msg,chat = ch,user = fromUser)
    return JsonResponse(data, safe=False)
