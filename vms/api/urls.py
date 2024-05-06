
from django.urls import path
from .views import *
urlpatterns = [
    path('vendors/',VendorView.as_view(),name="vendors"),
    path('vendors/<int:id>/',VendorView.as_view(),name="vendors"),
]
