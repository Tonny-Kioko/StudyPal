from urllib import response
from wsgiref import headers
import requests 
from requests.auth import HTTPBasicAuth
import json

def lipa_na_mpesa():

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = ("Authorization" "Bearer %s")
    request = {
    "BusinessShortCode":"174379",    
    "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMTYwMjE2MTY1NjI3",    
    "Timestamp":"20160216165627",    
    "TransactionType": "CustomerPayBillOnline",    
    "Amount":"1",    
    "PartyA":"254715150317",    
    "PartyB":"174379",    
    "PhoneNumber":"254715150317",    
    "CallBackURL":"https://studypal.com/domain/",    
    "AccountReference":"Test",    
    "TransactionDesc":"Test"
    }

    response = requests.post(api_url, json=request, headers=headers)
    print(response.text)

    lipa_na_mpesa()

# def getAccessToken(request):
#     consumer_key = "KlFs2XibD5jFbvOn1LP6RVscfw6bJDsh"
#     consumer_secret= "DkFK6yyerjTGUItB"
#     api_url
#     r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
#     mpesa_access_token = json.loads(r.text)
#     validated_mpesa_access_token = mpesa_access_token['access_token']
#     print(validated_mpesa_access_token)

#     return request