
from django.urls import path
from .views import *
urlpatterns = [
    path('vendors/',VendorView.as_view()),
    path('vendors/<int:id>/',VendorView.as_view()),
    path('purchase_orders/',PurchaseOrderView.as_view()),
    path('purchase_orders/<int:id>/',PurchaseOrderView.as_view()),
    path('purchase_orders/<int:id>/acknowledge/',AcknowledgeView.as_view())
]
