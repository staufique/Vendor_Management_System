import random
import string
from django.db import models
# import datetime
from django.utils import timezone
# Create your models here.
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Vendor(models.Model):
    name = models.CharField(max_length=150)
    contact_details = models.TextField(max_length=250)
    address = models.TextField(max_length=250)
    vendor_code = models.CharField(max_length=100,unique=True)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fullfillment_rate = models.FloatField(null=True)


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100,unique=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=timezone.now())
    delivery_date = models.DateTimeField(auto_now=timezone.now())
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100,default="pending")
    quality_rating = models.FloatField()
    issue_date = models.DateTimeField(auto_now=timezone.now())
    acknowledgement_date = models.DateTimeField()

    # def save(self, *args, **kwargs):
    #     # Generate a random string of length 10
    #     random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    #     self.po_number = random_string
    #     super().save(*args, **kwargs)

@receiver(pre_save, sender=PurchaseOrder)
def generate_po_number(sender, instance, **kwargs):
    if not instance.po_number:  # Only generate if po_number is not set
        random_string = ''.join(random.choices(string.digits, k=10))
        instance.po_number = random_string

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_rate = models.FloatField()
    average_response_time = models.FloatField()
    fullfillment_rate = models.FloatField()