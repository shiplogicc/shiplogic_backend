from django.db import models

# Create your models here.

from location.models import *
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user                = models.ForeignKey(User,null = False,db_index = True)
    name                = models.CharField(max_length=100)
    code                = models.CharField(max_length=30)
    activation_status   = models.BooleanField(blank=True)
    activation_date     = models.DateField(blank=True,null=True)
    remittance_cycle    = models.SmallIntegerField(default=7)
    added_on          = models.DateTimeField(auto_now_add=True)
    added_by          = models.ForeignKey(User,related_name='created_by', blank=True,null=True)
    updated_on          = models.DateTimeField(auto_now=True)
    updated_by          = models.ForeignKey(User,related_name='updated_by', blank=True,null=True)
    address             = models.ForeignKey(Address2, blank=True,null=True)
    contact_person      = models.ForeignKey(Contact,blank=True,null=True)
    pan_number          = models.CharField(max_length=20,blank=True,null=True)
    Gst_number          = models.CharField(max_length=20,blank=True,null=True)
    website             = models.CharField(max_length=200,blank=True,null=True)
    email               = models.CharField(max_length=200,blank=True,null=True)
    approved_by            = models.ForeignKey(User,related_name='approver',blank=True,null=True)
    bill_delivery_email = models.BooleanField(default=True)
    bill_delivery_hand  = models.BooleanField(default=True)
    referred_by         = models.CharField(max_length=30,blank=True,null=True)
    
    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name + " - " + self.code


class Role(models.Model):
    name = models.Charfield(max_length = 50,null = False,)
    role_url = models.Charfield(max_length = 100,null = False,)
    activatio_status = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now = True)



class CustomerEmployee(models.Model)
    user = models.ForeignKey(User,null = False)
    customer = models.ForeignKey(Customer,db_index = True,null = False)
    name = models.Charfield(max_length = 100,null = False,)
    email = models.Charfield(max_length = 150,null = False,)
    mobile_no = models.Charfield(max_length = 20,null = False,) 
    activation_status = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now = True)
    role_access = models.ManyToManyField(role)


    class Meta():
        unique_together = [['customer', 'email','mobile_no']]


