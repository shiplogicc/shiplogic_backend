from django.db import models

# Create your models here.

from location.models import *
from django.contrib.auth.models import User
from customer.models import *
# Create your models here.


class UserLogin(models.Model):
    user = models.OneToOneField(User,on_delete = models.SET_NULL,null = True,blank = True)
    fullname = models.CharField(max_length = 250,null = False,)
    mobile = models.CharField(max_length = 15,null = False,db_index = True)
    user_type = models.CharField(max_length = 50,null = False)
    email = models.CharField(max_length = 250,null = False,db_index = True)
    mobile_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    is_password_set = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now = True)
    status = models.IntegerField(default = 0,db_index = True)
    customer = models.ForeignKey(Customer,on_delete = models.SET_NULL,null = True,blank = True)
    profile_verified = models.BooleanField(default=False)


class Role(models.Model):
    name = models.CharField(max_length = 50,null = False,)
    role_url = models.CharField(max_length = 100,null = False,)
    activatio_status = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now = True)



class CustomerEmployee(models.Model):
    '''
    Relevance to be identified ?
    '''
    parent_user = models.ForeignKey(User,null = True,on_delete = models.SET_NULL,related_name = "parent_user")
    child_user = models.ForeignKey(User,null = True,on_delete = models.SET_NULL,related_name = "child_user")
    customer = models.ForeignKey(Customer,db_index = True,null = True,on_delete = models.SET_NULL)
    name = models.CharField(max_length = 100,null = False,)
    email = models.CharField(max_length = 150,null = False,)
    mobile_no = models.CharField(max_length = 20,null = False,) 
    activation_status = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now = True)
    role_access = models.ManyToManyField(Role)


    class Meta():
        unique_together = [['customer', 'email','mobile_no'],['parent_user','child_user']]




class UserSecretCredentials(models.Model):

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    client_id = models.CharField(max_length =250, null=True, blank=True)

    client_secret = models.CharField(max_length =250, null=True, blank=True)

    status = models.IntegerField(default=1, db_index=True)

    added_on = models.DateTimeField(auto_now_add=True, db_index=True)

    updated_on = models.DateTimeField(null=True, blank=True, db_index=True)




class UserDocumentDetails(models.Model):
    user = models.ForeignKey(UserLogin,null = True,on_delete = models.SET_NULL)
    document_name = models.CharField(max_length =250, null=True, blank=True)
    document_parameters = models.JSONField(null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(null=True, blank=True, db_index=True)





class BackgroundVerificationSetting(models.Model):
    verification_key  = models.CharField(max_length = 250, db_index = True, null = True, blank = True)
    url               = models.CharField(max_length = 250, db_index = True, null = True, blank = True)
    username          = models.CharField(max_length=75, db_index=True, null = True, blank = True)
    password          = models.CharField(max_length=75, db_index=True, null = True, blank = True)
    module            = models.CharField(max_length=75, db_index=True, null = True, blank = True)
    process_function  = models.CharField(max_length=75, db_index=True, null = True, blank = True)
    logging_required  = models.IntegerField(default=0, db_index=True)
    added_on          = models.DateTimeField(auto_now_add = True, db_index = True)
    updated_on        = models.DateTimeField(auto_now = True, db_index = True)
    activation_status = models.BooleanField(default = True,  db_index = True)
    verification_value  = models.CharField(max_length = 250, null = True, blank = True)
    def __unicode__(self):
        return str(self.verification_key) + " - "+ str(self.activation_status)



