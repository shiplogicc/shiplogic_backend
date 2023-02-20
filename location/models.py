from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length = 100,null = False)
    shortcode = models.CharField(max_length = 20,null = False)
    added_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    activation_status= models.BooleanField(default = True)

class State(models.Model):
    name = models.CharField(max_length = 100,null = False)
    country = models.ForeignKey(Country,limit_choices_to = {"activation_status":True},null = True,on_delete = models.SET_NULL)
    state_shortcode = models.CharField(max_length = 20,null = False,)
    added_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    activation_status= models.BooleanField(default = True)

    class Meta():
        unique_together = [['name', 'state_shortcode']]

class City(models.Model):
    name = models.CharField(max_length = 100,null = False,db_index = True,)
    state = models.ForeignKey(State,limit_choices_to = {"activation_status":True},null = True,on_delete = models.SET_NULL,)
    city_shortcode = models.CharField(max_length = 20,null = False,db_index = True,unique=True)
    added_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    activation_status= models.BooleanField(default = True)

    class Meta():
        unique_together = [['name', 'state']]


class Pincode(models.Model):
    pincode = models.IntegerField(null = False,db_index = True,unique=True)
    added_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    activation_status= models.BooleanField(default = True)
    city = models.ForeignKey(City,db_index = True,null = True,on_delete = models.SET_NULL,)

    

class Address(models.Model):
    address_line1 = models.CharField(max_length = 256,null = False,blank = False)
    address_line2 = models.CharField(max_length = 256,null = False,blank = False)
    address_line3 = models.CharField(max_length = 256,null = False,blank = False)
    city = models.ForeignKey(City,db_index = True,null = True,on_delete = models.SET_NULL,)
    pincode =  models.ForeignKey(Pincode,db_index = True,null = True,on_delete = models.SET_NULL,related_name = "address_pincode")
    activation_status= models.BooleanField(default = True)
    added_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    



class Contact(models.Model):
    name     = models.CharField(max_length=100)
    designation = models.CharField(max_length=100,blank=True,null=True)
    email    = models.CharField(max_length=100, default="", blank=True,null=True)
    address_line1 = models.CharField(max_length = 256,null = False,blank = False)
    address_line2 = models.CharField(max_length = 256,null = False,blank = False)
    address_line3 = models.CharField(max_length = 256,null = False,blank = False)
    city = models.CharField(max_length = 100,null = False,blank = False)
    pincode = models.CharField(max_length = 100,null = False,blank = False)
    phone = models.CharField(max_length=15, default="",blank=True,null=True)

    def __unicode__(self):
        return self.name    
