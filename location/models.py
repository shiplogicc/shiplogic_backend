from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.Charfield(max_length = 100,null = False)
    shortcode = models.Charfield(max_length = 20,null = False)
    added_on = models.DateTimeField(add_now_add = True)
    updated_on = models.DateTimeField(add_now = True)
    activation_status= models.BooleanField(default = True)

class State(models.Model):
    name = models.Charfield(max_length = 100,null = False)
    country = models.ForeignKey(Country,limit_choices_to = {"activation_status":True},null = False,)
    state_shortcode = models.Charfield(max_length = 20,null = False,)
    added_on = models.DateTimeField(add_now_add = True)
    updated_on = models.DateTimeField(add_now = True)
    activation_status= models.BooleanField(default = True)

    class Meta():
        unique_together = [['name', 'state_shortcode']]

class City(models.Model):
    name = models.Charfield(max_length = 100,null = False,db_index = True,)
    state = models.ForeignKey(State,limit_choices_to = {"activation_status":True},null = False,)
    city_shortcode = models.Charfield(max_length = 20,null = False,db_index = True,unique=True)
    added_on = models.DateTimeField(add_now_add = True)
    updated_on = models.DateTimeField(add_now = True)
    activation_status= models.BooleanField(default = True)

    class Meta():
        unique_together = [['name', 'state__id']]


class Pincode(models.Model):
    pincode = models.IntergerField(null = False,db_index = True,unique=True)
    added_on = models.DateTimeField(add_now_add = True)
    updated_on = models.DateTimeField(add_now = True)
    activation_status= models.BooleanField(default = True)
    city = models.ForeignKey(City,db_index = True,null = False)

    

    
