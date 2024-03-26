from requests import request
from django.http import HttpResponse, JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth
import json
from django.shortcuts import render, redirect
import os
from base.models import User
from mpesa.models import *
from .views import *
from .urls import *
#from mpesa.mpesa_credentials import LipanaMpesaPassword, MpesaAccessToken

from mpesa.mpesa_credentials import *

# try:
#     cart = CheckoutOrder.objects.get(user=request.username, status='Pending')
#     order = CheckoutOrder.objects.get(user=request.username, cart=cart)
# except CheckoutOrder.DoesNotExist:
#     # handle case when cart for user does not exist
#     pass



# print(f"checkout_order = {CheckoutOrder.objects.get(id=order.id)}")




def getAccessToken(request):
    consumer_key = os.environ.get('CONSUMER_KEY')
    consumer_secret = os.environ.get('CONSUMER_SECRET')
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    if r.status_code == 200:
        mpesa_access_token = json.loads(r.text)
        validated_mpesa_access_token = mpesa_access_token['access_token']
        return HttpResponse(validated_mpesa_access_token)
    else:
        return HttpResponse("Failed to generate access token")


def lipa_na_mpesa_online(request):
    if not request.user.is_authenticated:
        return redirect('studypal:login')
               
    phone_number = request.user.phone_number
    cart = CartObject(request)
    bill_amount = cart.get_total_price_after_discount()

    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {"Authorization": "Bearer %s" % access_token}
    mpesa_request = {
        "BusinessShortCode" : LipanaMpesaPassword.business_short_code, 
        "Password" : LipanaMpesaPassword.decode_password, 
        "Timestamp": LipanaMpesaPassword.lipa_time, 
        "TransactionType": "CustomerPayBillOnline", 
        "Amount" :  1,
        "PartyA": 'phone_number',
        "PartyB" : LipanaMpesaPassword.business_short_code, 
        "PhoneNumber" : 'phone_number', 
        "CallBackURL" : "https://sandbox.safaricom.co.ke/mpesa/", 
        "AccountReference" : "TruewaysEnterprisesLimited", 
        "TransactionDesc" : "Making Payment to Trueways for products under order number"
    }
    response = requests.post(api_URL, json=mpesa_request, headers=headers)
    context = {'access_token': access_token, 'api_URL':api_URL, 'headers':headers, 'request': request}
    if response.status_code == 200:        
        return render(request, 'password_prompt.html' )
    else:
        error_message = response.json()['errorMessage']
        print(error_message)
        print(phone_number)
        return HttpResponse("The payment was Unsuccessful")


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_URL = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {
        "ShortCode" : "LipanaMpesaPassword.business_short_code",
        "ResponseType" : "Completed/Cancelled", 
        "ConfirmationURL" : "https://595b-41-72-198-62.ngrok-free.app/api/v1/c2b/confirmation",
        "ValidationURL": "https://595b-41-72-198-62.ngrok-free.app/api/v1/c2b/validation" 
    }

    response = requests.post(api_URL, json = options, headers= headers)
    return HttpResponse(response.text) 


@csrf_exempt
def call_back(request):
    pass


@csrf_exempt
def validation(request):
    context = {
        "ResultCode" : 0, 
        "ResultDesc" : "Accepted"
    }
    return  JsonResponse(dict(context))


@csrf_exempt
def confirmation(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    payment = MpesaPayment(
        first_name = mpesa_payment['FirstName'],
        middle_name = mpesa_payment['MiddleName'],
        last_name = mpesa_payment['LastName'], 
        description = mpesa_payment['TransID'],
        phone_number = mpesa_payment['MSISDN'], 
        amount = mpesa_payment['TransAmount'],
        reference = mpesa_payment['BillRefNumber'], 
        organization_balance = mpesa_payment['OrgAccountBalance'], 
        type = mpesa_payment['TransactionType'], 
    )
    payment.save()
    context = {
        "ResultCode" : 0, 
        "ResultDesc" : "Accepted"
    }
    #return JsonResponse(dict(context))
    if mpesa_payment['ResultCode'] == 0:
        return render(request, 'payment_success.html')
    else:
        return redirect(request, 'payment_unsuccessful.html')
