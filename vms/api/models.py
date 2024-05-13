import random
import string
from django.db import models
# import datetime
from django.utils import timezone
# Create your models here.
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from datetime import timedelta
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db.models import Avg, F, ExpressionWrapper, fields
from django.contrib.auth.models import User
import os
from dotenv import load_dotenv
load_dotenv()

from django.contrib.auth.models import User
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

    def __str__(self):
        return f"{self.name}"
    
        

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100,unique=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(default=timezone.now()+timedelta(days=7))
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100,default="pending")
    quality_rating = models.FloatField()
    issue_date = models.DateTimeField(default=timezone.now)
    acknowledgement_date = models.DateTimeField(null=True)
        
    def save(self, *args, **kwargs):
        if not self.delivery_date:
            self.delivery_date = self.order_date + timedelta(days=7)
        super().save(*args, **kwargs)

    

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_rate = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fullfillment_rate = models.FloatField(null=True)

    def __str__(self):
        return f"{self.vendor} - {self.date}"

@receiver(pre_save, sender=PurchaseOrder)
def generate_po_number(sender, instance, **kwargs):
    if not instance.po_number:  # Only generate if po_number is not set
        random_string = ''.join(random.choices(string.digits, k=10))
        instance.po_number = random_string

@receiver(pre_save, sender=PurchaseOrder)
def calculate_total_quantity(sender, instance, **kwargs):
    if not instance.quantity:
        total_quantity = sum(instance.items.values())
        instance.quantity = total_quantity


@receiver(post_save, sender=PurchaseOrder)
def notify_vendor(sender, instance, created, **kwargs):
    if created:
        # Compose email content
        subject = 'New Purchase Order Notification'
        html_content = render_to_string('purchase_order_notification_email.html', {'purchase_order': instance})
        from_email = os.getenv('EMAIL_ID')  # Use your own email address
        to_email = instance.vendor.email  # Assuming contact_details contain the vendor's email address

        # Create EmailMessage object
        email = EmailMessage(subject, html_content, from_email, [to_email])
        email.content_subtype = 'html'  # Set email content type as HTML

        # Send email
        email.send()

@receiver(post_save, sender=PurchaseOrder)
def notify_to_vendor_for_status_updating(sender, instance, **kwargs):
    vendor = instance.vendor
    purchase_orders = PurchaseOrder.objects.filter(vendor=vendor, po_number=instance.po_number,acknowledgement_date__isnull=False)
    if purchase_orders.exists():
        subject = 'Update Purchase Order'
        html_content = render_to_string('update_order_status.html', {'purchase_order': instance})
        from_email = os.getenv('EMAIL_ID')  # Use your own email address
        to_email = instance.vendor.email  # Assuming contact_details contain the vendor's email address

        # Create EmailMessage object
        email = EmailMessage(subject, html_content, from_email, [to_email])
        email.content_subtype = 'html'  # Set email content type as HTML
        # Send email
        email.send()


@receiver(post_save, sender=PurchaseOrder)
def notify_buyer(sender, instance, **kwargs):
    vendor = instance.vendor
    user_id = instance.user_id
    purchase_orders = PurchaseOrder.objects.filter(vendor=vendor, po_number=instance.po_number,acknowledgement_date__isnull=False)
    if purchase_orders.exists():
        subject = 'Order Updates'
        html_content = render_to_string('track_order.html', {'purchase_order': instance})
        from_email = os.getenv('EMAIL_ID')  # Use your own email address
        to_email = instance.user_id.email  # Assuming contact_details contain the vendor's email address

        # Create EmailMessage object
        email = EmailMessage(subject, html_content, from_email, [to_email])
        email.content_subtype = 'html'  # Set email content type as HTML
        # Send email
        email.send()

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_average_time_rate(sender, instance, **kwargs):
    vendor = instance.vendor
    purchase_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgement_date__isnull=False)
    if purchase_orders.exists():
        #calculating average response time
        avg_expression = ExpressionWrapper(Avg(F('acknowledgement_date') - F('issue_date')), output_field=fields.DurationField())
        average_time_rate = purchase_orders.aggregate(average_time_rate=avg_expression)['average_time_rate']
        avg_res_time = str(average_time_rate).split(":")
        avg_res_time = int(avg_res_time[0])*3600 + int(avg_res_time[1])*60 + int(avg_res_time[2][0:2])

        #calculating on time delivery
        total_delivered_orders = PurchaseOrder.objects.filter(vendor=vendor, status='delivered').count()
        on_time_delivered_orders = PurchaseOrder.objects.filter(vendor=vendor, status='delivered', acknowledgement_date__isnull=False).count()
        on_time_delivery_rate = (on_time_delivered_orders / total_delivered_orders) * 100 if total_delivered_orders != 0 else 0
        
        # Calculate quality rating average
        quality_rating_avg = PurchaseOrder.objects.filter(vendor=vendor).aggregate(Avg('quality_rating'))['quality_rating__avg']
        
        # Calculate fulfillment rate
        total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
        fulfilled_orders = PurchaseOrder.objects.filter(vendor=vendor, status='delivered').count()
        fulfillment_rate = (fulfilled_orders / total_orders) * 100 if total_orders != 0 else 0

        # Update Vendor model
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.average_response_time = avg_res_time
        vendor.quality_rating_avg = quality_rating_avg
        vendor.fullfillment_rate = fulfillment_rate
        vendor.save()

         # Create or update HistoricalPerformance record
        HistoricalPerformance.objects.create(
            vendor=vendor,
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_rate=quality_rating_avg,
            average_response_time=avg_res_time,
            fullfillment_rate=fulfillment_rate
        )

