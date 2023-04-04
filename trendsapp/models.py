from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class shopregmodel(models.Model):
    shopname=models.CharField(max_length=50)
    shopid=models.IntegerField()
    location=models.CharField(max_length=50)
    email=models.EmailField()
    password=models.CharField(max_length=50)
    def __str__(self):
        return self.shopname

class productupmodel(models.Model):
    Category = (
        ('womenclothing', 'Women clothing'),
        ('womenwatch', 'Women watch'),
        ('womenshoe', 'Women shoe'),
        ('womenbag', 'Women bag'),
        ('menclothing', 'Men clothing'),
        ('menwatch', 'Men watch'),
        ('menshoe', 'Men shoe'),
        ('menbag', 'Men bag'),
    )
    Gendertype = (
        ('women', 'Women'),
        ('men', 'Men'),
    )
    shopid = models.IntegerField()
    productname=models.CharField(max_length=50)
    productprice=models.IntegerField()
    producttype=models.CharField(choices=Gendertype,max_length=20)
    category=models.CharField(choices=Category,max_length=50)
    description=models.CharField(max_length=100)
    productimage=models.ImageField(upload_to='trendsapp/static')
    def __str__(self):
        return self.productname



class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)


class cart(models.Model):
    productname = models.CharField(max_length=30)
    productprice = models.IntegerField()
    description = models.CharField(max_length=100)
    productimage = models.ImageField()
    userid = models.IntegerField()
    def __str__(self):
        return self.productname


class wishlist(models.Model):
    productname = models.CharField(max_length=30)
    productprice = models.IntegerField()
    description = models.CharField(max_length=100)
    productimage = models.ImageField()
    userid = models.IntegerField()
    def __str__(self):
        return self.productname

class buy(models.Model):
    productname = models.CharField(max_length=30)
    productprice = models.IntegerField()
    description = models.CharField(max_length=100)
    productimage = models.ImageField()
    quantity = models.IntegerField()
    def __str__(self):
        return self.productname

class cardmodels(models.Model):
    cardnumber = models.IntegerField()
    holdername = models.CharField(max_length=30)
    expire = models.CharField(max_length=30)
    ccv = models.IntegerField()
    def __str__(self):
        return self.holdername

class shopnotify(models.Model):
    content = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content

class usernotify(models.Model):
    content = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content