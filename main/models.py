from __future__ import unicode_literals

from django.db import models
#from django.contrib.auth.models import AbstractUser


#class User(AbstractUser):
#    user_type = models.CharField(max_length=30, default='Patient')

class Usr(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=100, default="patient")
    extra = models.CharField(max_length=100, default="Nephrology")
    balance = models.IntegerField(default=0)
    

class Consultation(models.Model):
    c_id = models.CharField(max_length=100, unique=True)
    patient = models.CharField(max_length=100)
    patient_name = models.CharField(max_length=100)
    doctor = models.CharField(max_length=100)
    doc_name = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    comments = models.TextField()
    active = models.BooleanField(default=True)

class Payment(models.Model):
    user = models.CharField(max_length=100)
    payment_type = models.CharField(max_length=100)
    item_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, unique=True)
    status = models.IntegerField(default=0) #possible states are initiated-0, pending-1, success-2, failure-3
    active = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    date = models.DateField()

class Room(models.Model):
    user_id = models.CharField(max_length=100)
    r_id = models.CharField(max_length=100, unique=True)
    room_no = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    available = models.BooleanField(default=True)

class Notification(models.Model):
    n_id = models.CharField(max_length=100, unique=True)
    patient = models.CharField(max_length=100)
    doc_name = models.CharField(max_length=100)
    date = models.DateField()
    
class Appointment(models.Model):
    a_id = models.CharField(max_length=100, unique=True)
    patient_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    doctor = models.CharField(max_length=100)
    doc_name = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    token = models.IntegerField(default=1)
    time = models.DateField()

class Prescription(models.Model):
    user_id = models.CharField(max_length=100)
    p_id = models.CharField(max_length=100, unique=True)
    doctor = models.CharField(max_length=100)
    medicine_name = models.CharField(max_length=100)
    details = models.TextField()
    active = models.BooleanField(default=True)

class Medicine(models.Model):
    m_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
