from django import forms

class shopregform(forms.Form):
    shopname=forms.CharField(max_length=50)
    shopid=forms.IntegerField()
    location=forms.CharField(max_length=50)
    email=forms.EmailField()
    password=forms.CharField(max_length=50)
    confirmpassword=forms.CharField(max_length=50)


class shoplogform(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(max_length=50)

class productupform(forms.Form):
    Category = (
        ('select', 'Select'),
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
    productname=forms.CharField(max_length=50)
    productprice=forms.IntegerField()
    producttype=forms.CharField(label='Type', widget=forms.RadioSelect(choices=Gendertype))
    category=forms.CharField(label='Category', widget=forms.RadioSelect(choices=Category))
    description=forms.CharField(max_length=100)
    productimage=forms.ImageField()


class cardforms(forms.Form):
    cardnumber = forms.IntegerField()
    holdername = forms.CharField(max_length=30)
    expire = forms.CharField(max_length=30)
    ccv = forms.IntegerField()

