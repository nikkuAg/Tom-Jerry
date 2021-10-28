from django.http.response import HttpResponse
from django.shortcuts import render
import requests
from rest_framework import viewsets
from .models import User, Request_Sent, Request_Confirm, Audit
from .serializers import UserSerializer, SentSerializer, ConfirmSerializer, AuditSerializer
import requests
import json
import base64
import uuid
from PIL import Image
import zipfile36 as zipfile
from zipfile import ZipFile
import xmltodict
import os
import io
import xml.etree.ElementTree as ET
from django.http import JsonResponse
import random
import string
# Create your views here.

otpTxnNumber = ""
uid = "999988636660"
captchaTxnId = ""


class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SentViewSets(viewsets.ModelViewSet):
    queryset = Request_Sent.objects.all()
    serializer_class = SentSerializer


class ConfirmViewSets(viewsets.ModelViewSet):
    queryset = Request_Confirm.objects.all()
    serializer_class = ConfirmSerializer


class AuditViewSets(viewsets.ModelViewSet):
    queryset = Audit.objects.all()
    serializer_class = AuditSerializer


def capchaViewset(request):
    # chaViewset()
    global captchaTxnId
    captcha_url = "https://stage1.uidai.gov.in/unifiedAppAuthService/api/v2/get/captcha"
    data = {
        "langCode": "en",
        "captchaLength": "3",
        "captchaType": "2"
    }
    headers = {
        "Content-Type": "application/json"
    }
    res = requests.post(captcha_url, data=json.dumps(data),
                        headers=headers, verify=True)
    base64_str = res.json()['captchaBase64String']
    print("txn id")
    print(res.json()['captchaTxnId'])
    captchaTxnId = res.json()['captchaTxnId']

    out = base64.b64decode(base64_str)
    savepath = os.path.join('./captcha.png')
    img = Image.open(io.BytesIO(out))
    img.save(savepath)
    return HttpResponse(base64_str)


def otpGeneratorViewset(request):
    headers = {"Content-Type": "application/json", "x-request-id": str(uuid.uuid4()),
               "appid": "MYAADHAAR", "Accept-Language": "en_in"}
    otp_url = "https://stage1.uidai.gov.in/unifiedAppAuthService/api/v2/generate/aadhaar/otp"
    txnId = str(uuid.uuid4())
    value = input("c? ")
    data = {
        "uidNumber": '999988636660',
        "captchaTxnId": captchaTxnId,
        "captchaValue": value,
        "transactionId": f"MYAADHAAR:{txnId}"
    }
    print(data)
    # uid = request.uid
    response = requests.post(otp_url, data=json.dumps(data),
                             headers=headers, verify=True)
    print(response.json())
    global otpTxnNumber
    otpTxnNumber = response.json()['txnId']
    return HttpResponse(response)


def passwordGenerator():
    length = 10
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits

    mixString = lower + upper + num

    password = random.sample(mixString, length)

    return password


def eKYC(request):
    otp = input("o? ")
    ekyc_url = "https://stage1.uidai.gov.in/eAadhaarService/api/downloadOfflineEkyc"
    print(otp)
    headers = {
        "Content-Type": "application/json", "X-Request-ID": str(uuid.uuid4()), "appID": "PORTAL", "transactionId": str(uuid.uuid4())
    }
    data = {
        "aadhaarOrVidNumber": 0, "txnNumber": f"{otpTxnNumber}", "shareCode": "1729", "otp": f"{otp}",
        "deviceId": None, "transactionId": None, "unifiedAppRequestTxnId": None, "uid": uid, "vid": None
    }
    print(data)

    res = requests.post(ekyc_url, data=json.dumps(data),
                        headers=headers, verify=True)
    # print(res.json())
    ################################ Unzipping xml data ################################
    ekyc_bytes = base64.b64decode(res.json()['eKycXML'])
    password = passwordGenerator()
    print("password ", password)
    with open("ekyc.zip", "wb") as zip_file:
        zip_file.write(ekyc_bytes)
    with ZipFile("ekyc.zip") as f:
        f.extractall(pwd=password)

    prefixed = [filename for filename in os.listdir(
        '.') if filename.startswith("offlineaadhaar")]
    with open(prefixed[0]) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    json_data = json.dumps(data_dict)
    print(json_data)
    os.remove(prefixed[0])
    os.remove("captcha.png")
    os.remove("ekyc.zip")

    return HttpResponse("done")
