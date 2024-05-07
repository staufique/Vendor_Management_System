from django.shortcuts import render

# Create your views here.
from .models import *
from .serializers import *
from django.http import JsonResponse
from rest_framework.views import APIView
from django.utils import timezone
from datetime import datetime
class VendorView(APIView):

    def get(self,request,id=None):
        if id:
            data = Vendor.objects.filter(id=id).first()
            if data is None:
                return JsonResponse("data is not present",safe=False)
            serializer = VendorSerializer(data)
            return JsonResponse(serializer.data, safe=False)
        data = Vendor.objects.all()
        serializer = VendorSerializer(data,many=True)
        return JsonResponse(serializer.data,safe=False)
    
    def post(self,request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)
    
    def put(self,request,id):
        if id:
            data = Vendor.objects.filter(id=id).first()
            serializer = VendorSerializer(data,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,safe=True)
            return JsonResponse("inside",safe=False)
        return JsonResponse("wrong",safe=False)
       
    def delete(self,request,id=None):
        data = Vendor.objects.filter(id=id).first()
        if data is None:
            return JsonResponse("invalid id",safe=False)
        data.delete()
        return JsonResponse("data deleted",safe=False)

class PurchaseOrderView(APIView):
    def get(self,request,id=None):
        if id:
            data = PurchaseOrder.objects.filter(id=id).first()
            if data is None:
                return JsonResponse("invalid id",safe=False)
            serializer = PurchaseOrderSerializer(data)
            return JsonResponse(serializer.data,safe=False)
        data = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(data,many=True)
        return JsonResponse(serializer.data,safe=False)
    
    def post(self,request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,safe=False)
        return JsonResponse(serializer.errors)
    
    def put(self,request,id):
        if id:
            data = PurchaseOrder.objects.filter(id=id).first()
            serializer = PurchaseOrderSerializer(data,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,safe=True)
            return JsonResponse("inside",safe=False)
        return JsonResponse("wrong",safe=False)
       
    def delete(self,request,id=None):
        data = PurchaseOrder.objects.filter(id=id).first()
        if data is None:
            return JsonResponse("invalid id",safe=False)
        data.delete()
        return JsonResponse("data deleted",safe=False)
    
class AcknowledgeView(APIView):
    def get(self,request,id=None):
        if id:
            po_id = PurchaseOrder.objects.filter(id=id).first()
            if id is None:
                return JsonResponse("order not found",saf=False)
            po_id.acknowledgement_date = timezone.now()
            # v = Vendor.objects.filter(id=po_id.vendor).first()
            serializer = PurchaseOrderSerializer(po_id,data=po_id)
            po_id.save()
            # str1 = str(po_id.acknowledgement_date - po_id.issue_date).split(":")
            # for i in range(len(str1)):
            #     if i==0:
            #         str1[i]=int(str1[i])*3600
            #     elif i==1:
            #         str1[i]=int(str1[i])*60
            #     elif i==2:
            #         str1[i]=int(str1[i][:2])
            # str2 = sum(str1)
            # v.average_response_time = float(str2)
            # v.save()
            serializer = PurchaseOrderSerializer(po_id)
            return JsonResponse(serializer.data)
        
        return JsonResponse("order not found",safe=False)


class CheckRatings(APIView):
    def get(self,request):

        data = PurchaseOrder.objects.filter(vendor=4).all()
        a=[]
        for i in data:
            if i.acknowledgement_date is None:
                continue
            a += [str(i.acknowledgement_date - i.issue_date).split(":")]
        a = [int(a[i][0])*3600 + int(a[i][1])*60 + int(float(a[i][2])) for i in range(len(a))]
        print("*********************",a)
        avg = sum(a)/len(a)
        print("************************",avg)
        serializer = PurchaseOrderSerializer(data,many=True)
        return JsonResponse(serializer.data,safe=False)

class DeliverView(APIView):

    def get(self,request,id,status):
        if status=="delivered":
            data = PurchaseOrder.objects.filter(id=id).first()
            if data.acknowledgement_date is None:
                return JsonResponse({'masg':"first acknowledged the order"})
            data.status = status
            data.save()
            serializer = PurchaseOrderSerializer(data)
            return JsonResponse(serializer.data)
        elif status=="cancelled":
            data = PurchaseOrder.objects.filter(id=id).first()
            data.status = status
            data.save()
            serializer = PurchaseOrderSerializer(data)
            return JsonResponse(serializer.data)
        return JsonResponse("something went wrong",safe=False)