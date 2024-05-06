from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name','contact_details','address','vendor_code',
                    'on_time_delivery_rate','quality_rating_avg','average_response_time','fullfillment_rate']