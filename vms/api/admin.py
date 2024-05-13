from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['id','name','contact_details','address','vendor_code',
                    'on_time_delivery_rate','quality_rating_avg','average_response_time','fullfillment_rate']
    
@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['id','user_id','po_number','vendor','order_date','delivery_date',
                    'items','quantity','status','quality_rating',
                    'issue_date','acknowledgement_date']
    
@admin.register(HistoricalPerformance)
class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = ['id','vendor','date','on_time_delivery_rate','quality_rating_rate','average_response_time','fullfillment_rate']