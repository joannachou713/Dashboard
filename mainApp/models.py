from django.db import models
from django import forms
from .forms import FormStatus
# Create your models here.


class Client(models.Model):
    client_name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=50, blank=True)
    
class Order(models.Model):
    # client_id = models.IntegerField()
    product = models.CharField(max_length=20)
    payment = models.IntegerField()
    quantity = models.IntegerField()
    order_time = models.DateField()
    channel= models.CharField(max_length=20)
    packing_cost = models.IntegerField()
    packing_time = models.DateField(blank=True)
    arrive_time = models.DateField(blank=True)

    client_id  = models.ForeignKey(Client, on_delete=models.CASCADE)

class Status(models.Model):
    SELVALUE = (
        ('已審核', '已審核'),
        ('備貨中', '備貨中'),
        ('已達包裹中心', '已達包裹中心'),
        ('已達物流中心', '已達物流中心'),
        ('已出貨', '已出貨'),
        ('已到達', '已到達'),
        ('已辦理退貨', '已辦理退貨'),
        ('退貨審核不通過', '退貨審核不通過')
    )
    response = models.CharField(default=0, choices=FormStatus.SELVALUE, verbose_name='response',max_length=20)