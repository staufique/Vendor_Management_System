from django.shortcuts import render

# Create your views here.
from .models import *
from .serializers import *
from django.http import JsonResponse
from rest_framework.views import APIView


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
        data = Vendor.objects.get(id=id)
        data.delete()
        return JsonResponse("data deleted",safe=False)