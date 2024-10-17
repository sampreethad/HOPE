from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class userProfile(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='profile_pic',default='sherlock.jpg')
    phone = models.CharField(max_length=500,blank=True)
    address = models.CharField(max_length=5000,blank=True)
    balance = models.IntegerField(default=30000)
    shopkeeperName = models.CharField(max_length=500,blank=True)
    shopkeeperAddress = models.CharField(max_length=500,blank=True)
    shopkeeperPhone = models.IntegerField(default=0)
    shopkeeperLocation = models.CharField(max_length=500,blank=True)
    shopType = models.CharField(max_length=500,blank=True)
    accountType = models.CharField(max_length=500,blank=True)
    hospitalName = models.CharField(max_length=500,blank=True)
    hospitalAddress = models.CharField(max_length=500,blank=True)
    hospitalPhone = models.IntegerField(default=0)
    hospitalLocation = models.CharField(max_length=500,blank=True)
    hospitalType = models.CharField(max_length=500,blank=True)
    district = models.CharField(max_length=1000,default = "")
    # models.CharField(max_length=500,blank=True)
    # deliveryManName = models.CharField(max_length=500,blank=True)
    # deliveryManAddress = models.CharField(max_length=500,blank=True)
    # deliveryManPhone = models.IntegerField(default=0)
    specialization = models.CharField(blank=True,default="",max_length=1500)
    added_by = models.CharField(blank=True,default="",max_length=1500)
    APPROVE = True
    REJECT = False
    CHOICES = (
        (APPROVE, 'Approve'),
        (REJECT, 'Reject')
    )
    # status = models.BooleanField(choices=CHOICES, default=REJECT)
    is_shopkeeper = models.BooleanField(choices=CHOICES, default=REJECT)
    is_hospital = models.BooleanField(choices=CHOICES, default=REJECT)
    is_doctor = models.BooleanField(default=False)
    reject = models.BooleanField(default=False)
    # is_delivery_man = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username +"'s " + self.accountType +" profile"


class Product(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    added_by = models.CharField(max_length=5000,blank=True)
    image = models.ImageField(upload_to='product',default='sherlock.jpg',blank=True)
    userImage = models.CharField(max_length=5000,blank=True)
    # transaction_address = models.CharField(max_length=5000,blank=True)
    name = models.CharField(max_length=5000,blank=True)
    dosage = models.CharField(max_length=5000,blank=True)
    price = models.IntegerField(default=0)
    activeIngredient = models.CharField(max_length=5000,blank=True)
    productType = models.CharField(max_length=5000,blank=True)
    route = models.CharField(max_length=5000,blank=True)
    manufacturerName = models.CharField(max_length=5000,blank=True)
    manufacturerAddress = models.CharField(max_length=5000,blank=True)
    manufacturerCountry = models.CharField(max_length=5000,blank=True)
    manufacturerContactNumber = models.CharField(max_length=5000,blank=True)
    
    stock = models.IntegerField(default=0)
    banned = models.BooleanField(default=False)

    sell = models.BooleanField(default=False)
    approved = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username + " product." + " Product name : "+ self.name
    

class Status(models.Model):
    username = models.CharField(max_length=500)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    transaction_address = models.CharField(max_length=5000,blank=True)
    
    def __str__(self):
        return "product status"


class Leave(models.Model):
    username = models.CharField(max_length=500)
    
    date = models.CharField(max_length=500)
    # transaction_address = models.CharField(max_length=5000,blank=True)
    
    def __str__(self):
        return self.username + " leave" 
    
class cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username +"'s cart." + " Product : " + self.product.name 
    

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    address = models.CharField(max_length=50000,default="")
    date = models.DateTimeField(auto_now_add= True)
    to = models.CharField(max_length=50000,default="",blank=True)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username + "'s order." + " Product : " + self.product.name
    

class Chat(models.Model):

    from_user = models.CharField(max_length = 1000)
    to_user = models.CharField(max_length = 1000)
    date = models.DateTimeField(auto_now_add = True)
    count = models.IntegerField(default=0)
    def __str__(self):
        return self.from_user + " to " + self.to_user
    
class Message(models.Model):
    chat = models.ForeignKey(Chat,on_delete = models.CASCADE)
    message = models.CharField(max_length = 10000)
    user = models.CharField(max_length = 10000)
    date = models.DateTimeField(auto_now_add = True)
    translation = models.CharField(max_length = 10000)
    def __str__(self) -> str:
        return self.message + " message" 
    


class Music(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='musicImg/')
    file = models.FileField(upload_to='music')
    artist = models.CharField(max_length=50000,default="")
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Blog(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='blog/')
    desc = models.CharField(max_length=50000,default="")
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Article"

class YogaClass(models.Model):
    name = models.CharField(max_length=100,blank = True)
    image =  models.ImageField(upload_to='videoImg/',blank = True)
    description = models.CharField(max_length=50000,default="")
    def __str__(self) -> str:
        return self.name
      
class videoSolution(models.Model):

    chapter = models.ForeignKey(YogaClass,on_delete=models.CASCADE,null = True,blank = True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='videoImg/')
    file = models.FileField(upload_to='videos')
    desc = models.CharField(max_length=50000,default="")
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Yoga Video"


class Enrollment(models.Model):
    username = models.CharField(max_length=100)
    yoga = models.ForeignKey(YogaClass,on_delete=models.CASCADE,null = True,blank = True)
    def __str__(self) -> str:
        return self.username

class Appointment(models.Model):

    username = models.CharField(max_length=500)
    doctor = models.CharField(max_length=500)
    date = models.CharField(max_length=500)
    time = models.CharField(max_length=500)
    symptoms = models.CharField(max_length=500)
    prescription = models.CharField(max_length=500)
    gender = models.CharField(max_length=500)
    blood = models.CharField(max_length=500)
    done = models.BooleanField(default=False)
    reject = models.BooleanField(default=False)
    file = models.FileField(upload_to='prescriptions',null = True,blank= True)
    def __str__(self):
        return self.doctor + "'s Appointment"
    
    class Meta:
        verbose_name = "Booking"

class Time(models.Model):

    username = models.CharField(max_length=500)
    time = models.CharField(max_length=500)

    def __str__(self):
        return "Time"

class Notification(models.Model):
    
    product_pk = models.IntegerField(default = 0)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.CharField(max_length=5000,blank=True,default ="")
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username + ' notification'
    

class Payment(models.Model):
    from_user = models.CharField(max_length=50000,default="")
    to_user = models.CharField(max_length=50000,default="")
    amount = models.CharField(max_length=50000,default="")
    product = models.CharField(max_length=50000,default="")
    def __str__(self):
        return self.from_user +  " paid Rs " + self.amount + " to " + self.to_user +" for the product " + self.product

class ShopKeeper(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    shopkeeperName = models.CharField(max_length=255)
    shopkeeperPhone = models.CharField(max_length=20)
    shopkeeperAddress = models.CharField(max_length=255)
    shopType = models.CharField(max_length=100)
    email = models.EmailField()
    APPROVE = True
    REJECT = False
    CHOICES = (
        (APPROVE, 'Approve'),
        (REJECT, 'Reject')
    )
    is_shopkeeper = models.BooleanField(choices=CHOICES,default=False)

    def __str__(self):
        return self.shopkeeperName
    
class Hospital(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    hospitalName = models.CharField(max_length=255)
    hospitalPhone = models.CharField(max_length=20)
    hospitalAddress = models.CharField(max_length=255)
    email = models.EmailField()
    APPROVE = True
    REJECT = False
    CHOICES = (
        (APPROVE, 'Approve'),
        (REJECT, 'Reject')
    )
    is_hospital = models.BooleanField(choices=CHOICES,default=False)

    def __str__(self):
        return self.hospitalName

class Doctor(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    specialization = models.CharField(max_length=255)
    APPROVE = True
    REJECT = False
    CHOICES = (
        (APPROVE, 'Approve'),
        (REJECT, 'Reject')
    )
    is_doctor = models.BooleanField(choices=CHOICES,default=False)

    class Meta:
        verbose_name = "Therapist"

    def __str__(self):
        return self.Name
    
@receiver(post_save, sender=ShopKeeper)
def update_user_profile(sender, instance, **kwargs):
    user_profile = userProfile.objects.get(user=instance.user)
    user_profile.is_shopkeeper = instance.is_shopkeeper
    user_profile.save()

@receiver(post_save, sender=Hospital)
def update_user_profile(sender, instance, **kwargs):
    user_profile = userProfile.objects.get(user=instance.user)
    user_profile.is_hospital = instance.is_hospital
    user_profile.save()

@receiver(post_save, sender=Doctor)
def update_user_profile(sender, instance, **kwargs):
    user_profile = userProfile.objects.get(user=instance.user)
    user_profile.is_doctor = instance.is_doctor
    user_profile.save()


class Comment(models.Model):
    username = models.CharField(max_length=1000)
    comment = models.CharField(max_length=10000)
    date = models.DateTimeField(auto_now_add=True)
    reply = models.CharField(max_length=10000,default="")
    def __str__(self):
        return self.username + " comment"
    
class Activity(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='activity/')
    link = models.CharField(max_length=100)
    desc = models.CharField(max_length=50000,default="")
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Yoga"

class userProfileApp(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
    image = models.ImageField(upload_to='profile_pic',default='sherlock.jpg')
    specialization = models.CharField(max_length=1000,blank=True,default="")
    phone = models.CharField(max_length=1000,blank=True,default="")
    address = models.CharField(max_length=1000,blank=True,default="")
    registered_as = models.CharField(default = "",max_length = 1000)
    is_doctor = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username + " profile"
    

class faq(models.Model):
    name = models.CharField(max_length=200)
    answer = models.CharField(max_length=5000)
    def __str__(self):
        return self.name + ":" + self.answer
