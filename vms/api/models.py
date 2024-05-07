import random
import string
from django.db import models
# import datetime
from django.utils import timezone
# Create your models here.
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from datetime import timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
import json

class Vendor(models.Model):
    name = models.CharField(max_length=150)
    contact_details = models.TextField(max_length=250)
    email = models.EmailField(max_length=100,default='')
    address = models.TextField(max_length=250)
    vendor_code = models.CharField(max_length=100,unique=True)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fullfillment_rate = models.FloatField(null=True)


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100,unique=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now())
    delivery_date = models.DateTimeField(default=timezone.now()+timedelta(days=7))
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100,default="pending")
    quality_rating = models.FloatField()
    issue_date = models.DateTimeField(default=timezone.now())
    acknowledgement_date = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.delivery_date:
            self.delivery_date = self.order_date + timedelta(days=7)
        super().save(*args, **kwargs)



class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_rate = models.FloatField()
    average_response_time = models.FloatField()
    fullfillment_rate = models.FloatField()


@receiver(pre_save, sender=PurchaseOrder)
def generate_po_number(sender, instance, **kwargs):
    if not instance.po_number:  # Only generate if po_number is not set
        random_string = ''.join(random.choices(string.digits, k=10))
        instance.po_number = random_string

@receiver(pre_save, sender=PurchaseOrder)
def calculate_total_quantity(sender, instance,**kwargs):
    if not instance.quantity:
        print("**********************",instance.items.values())

        total_quantity = sum(instance.items.values())
        instance.quantity = total_quantity
        instance.save()

@receiver(post_save, sender=PurchaseOrder)
def notify_vendor(sender, instance, created, **kwargs):
    if created:
        # Compose email content
        subject = 'New Purchase Order Notification'
        message = render_to_string('purchase_order_notification_email.html', {'purchase_order': instance})
        from_email = 'programswar@gmail.com'  # Use your own email address
        to_email = instance.vendor.email  # Assuming contact_details contain the vendor's email address

        # Send email
        send_mail(subject, message, from_email, [to_email])