
from django.urls import path
from .views import *
urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('vendors/',VendorView.as_view(),name='vendors'),
    path('vendors/<int:id>/',VendorView.as_view(),name='vendor_retrieve'),
    path('purchase_orders/',PurchaseOrderView.as_view(),name='purchase_order'),
    path('purchase_orders/<int:id>/',PurchaseOrderView.as_view(),name='purchase_order_retrive'),
    path('purchase_orders/<int:id>/acknowledge/',AcknowledgeView.as_view(),name='purchase_order_acknowledge'),
    path('status/<int:id>/<str:status>/',DeliverView.as_view(),name='deliver_status'),
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceView.as_view(), name='vendor_performance'),
    path('vendors/<int:vendor_id>/performance/<str:date>/', VendorPerformanceView.as_view(), name='vendor_performance_with_date'),
]

