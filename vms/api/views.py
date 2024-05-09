from functools import wraps
from django.shortcuts import redirect, render
import jwt

from django.conf import settings

# Create your views here.
from .models import *
from .serializers import *
from django.http import JsonResponse
from rest_framework.views import APIView
from django.utils import timezone
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }

class UserSignupView(APIView):
    def get(self,requuest):
        return Response("Signup Page")
    def post(self,request, *args, **kwargs):
        serializer = UserSigunUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response({'msg':'Register Successful'},status=status.HTTP_201_CREATED)
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserLoginView(APIView):
    def get(self, request):
        return Response("login")
    
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = User.objects.filter(email=email, password=password).first()
            if user is not None:
                token = get_tokens_for_user(user)
                response = JsonResponse({"token": token, "msg": "login success"}, status=status.HTTP_200_OK)
                response.set_cookie('access', str(token['access']))  
                response.set_cookie('refresh', str(token['refresh'])) 
                return response
            return Response({"errors": {"validation_errors": ['password and email are not valid']}}, status=status.HTTP_404_NOT_FOUND)


class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access')
        refresh_token = request.COOKIES.get('refresh')

        if access_token is None or refresh_token is None:
            return None
        try:
            access_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = access_payload['user_id']
            user = User.objects.get(pk=user_id)
          
            return (user, access_token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Access token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid access token')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        
class UserLogoutView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        response = JsonResponse({'msg': f'{request.user} Logout Successfully'}, status=status.HTTP_200_OK)
        response.delete_cookie('access')  
        response.delete_cookie('refresh')  
        return response

class VendorView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,id=None):
        if id:
            data = Vendor.objects.filter(id=id).first()
            if data is None:
                return JsonResponse("data is not present",safe=False)
            serializer = VendorSerializer(data,context={'request': request})
            return JsonResponse(serializer.data, safe=False)
        data = Vendor.objects.all()
        serializer = VendorSerializer(data,many=True,context={'request': request})
        return JsonResponse(serializer.data,safe=False)
    
    def post(self,request):

        if not request.user.is_superuser:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)
    
    def put(self,request,id):
        if not request.user.is_superuser:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        if id:
            data = Vendor.objects.filter(id=id).first()
            serializer = VendorSerializer(data,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,safe=True)
            return JsonResponse("inside",safe=False)
        return JsonResponse("wrong",safe=False)
       
    def delete(self,request,id=None):

        if not request.user.is_superuser:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        data = Vendor.objects.filter(id=id).first()
        if data is None:
            return JsonResponse("invalid id",safe=False)
        data.delete()
        return JsonResponse("data deleted",safe=False)

class PurchaseOrderView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,id=None):
        if id:
            data = PurchaseOrder.objects.filter(id=id).first()
            if data is None:
                return JsonResponse("invalid id",safe=False)
            serializer = PurchaseOrderSerializer(data,context={'request': request})
            return JsonResponse(serializer.data,safe=False)
        data = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(data,many=True,context={'request': request})
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
            serializer = PurchaseOrderSerializer(po_id,data=po_id)
            po_id.save()
            serializer = PurchaseOrderSerializer(po_id)
            return JsonResponse(serializer.data)
        
        return JsonResponse("order not found",safe=False)

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
    

class VendorPerformanceView(APIView):
    def get(self, request, vendor_id, date=None):
        vendor = Vendor.objects.filter(id=vendor_id).first()
        if vendor is None:
            return JsonResponse({"error": "Vendor not found"}, status=404)
        
        performances = HistoricalPerformance.objects.filter(vendor=vendor)
        
        if date:
            try:
                specified_date = datetime.strptime(date, "%Y-%m-%d").date()
                performances = performances.filter(date__date=specified_date)
            except ValueError:
                return JsonResponse({"error": "Invalid date format. Please provide date in YYYY-MM-DD format."}, status=400)

        performance_data = []
        
        for performance in performances:
            performance_data.append({
                "date": performance.date,
                "on_time_delivery_rate": performance.on_time_delivery_rate,
                "quality_rating_rate": performance.quality_rating_rate,
                "average_response_time": performance.average_response_time,
                "fullfillment_rate": performance.fullfillment_rate
            })

        return JsonResponse(performance_data, safe=False)