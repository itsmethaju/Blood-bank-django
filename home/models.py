from django.db import models

# Create your models here.

from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User

class BloodGroup(models.Model):
    name = models.CharField(max_length=5)
    image = models.ImageField(upload_to="")
    def __str__(self):
        return self.name



class Street(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    city = models.ForeignKey(
        'City', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-name"]



    

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

from django.db import models


class State(models.Model):
    name = models.CharField(max_length=30)
    stateimage = models.ImageField(upload_to="")

    def __str__(self):
        return self.name

class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    districtimage = models.ImageField(upload_to="")
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=10)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    vnuimage = models.ImageField(upload_to="")
    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.name


class Donor(models.Model):
    donor = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    date_of_birth = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)


    address = models.TextField(max_length=500, default="")
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)

    image = models.ImageField(upload_to="")
    ready_to_donate = models.BooleanField(default=True)

    def __str__(self):
        return str(self.blood_group)

class RequestBlood(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    address = models.CharField(max_length=500, blank=True)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE)
    date = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    message = models.CharField(max_length=500, blank=True)


    def __str__(self):
        return self.name