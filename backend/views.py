from django.http.response import HttpResponse, JsonResponse
import requests
from rest_framework import viewsets
from .models import Address, User, Request_Sent, Request_Confirm, Audit
from .serializers import PasswordSearilizer, UserSerializer, SentSerializer, ConfirmSerializer, AuditSerializer
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
import random
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
import random
from .encryption_util import *
from .permissions import *
from geopy.distance import geodesic
# Create your views here.

# otpTxnNumber = ""
# uid = "999916184317"
# captchaTxnId = ""


class UserViewSets(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usr = encrypt("999964798565")
        print(usr)
        queryset = User.objects.all()
        return queryset


class SentViewSets(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = Request_Sent.objects.all()
    serializer_class = SentSerializer
    permission_classes = [IsAuthenticated, SentReceivePermissions]

    def perform_create(self, serializer, *args, **kargs):
        serializer.save(client=self.request.user)


class ConfirmViewSets(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = Request_Confirm.objects.all()
    serializer_class = ConfirmSerializer
    permission_classes = [IsAuthenticated, SentReceivePermissions]

    def perform_create(self, serializer, *args, **kargs):
        serializer.save(introducer=self.request.user)


class AuditViewSets(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = Audit.objects.all()
    serializer_class = AuditSerializer
    permission_classes = [IsAuthenticated, AuditPermissions]


class PasswordView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, AuditPermissions]
    serializer_class = PasswordSearilizer

    def get_queryset(self):
        print("hfhfh")
        password = self.request.query_params.get('password')
        print(password)
        client = User.objects.get(id=self.request.user.id)
        Req = Request_Confirm.objects.filter(client=client)
        passwordattempt = Req[0].passAttempt
        passwordattempt = passwordattempt+1
        # return (password)
        if(password == Req[0].password):
            queryset = Req
            print('confirm')
            return queryset
        else:
            print('not confirm')
            print(passwordattempt)
            Req.update(passAttempt=(passwordattempt))
            return None


def capchaViewset(request):
    # global captchaTxnId
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

    # out = base64.b64decode(base64_str)
    # savepath = os.path.join('./captcha.png')
    # img = Image.open(io.BytesIO(out))
    # img.save(savepath)
    return JsonResponse({"image": base64_str, "trxnId": captchaTxnId})


def otpGeneratorViewset(request, capcha, id, uid):
    """"
    if captcha is invalid
    {'httpStatus': 'OK', 'message': 'Invalid Captcha', 'code': 400, 'transactionId': 'f7f600ab-592d-48dd-9c2f-513517f86872:MOBILE_NO',
        'traceCode': 'f7f600ab-592d-48dd-9c2f-513517f86872:MOBILE_NO', 'type': 'INVALID_CAPTCHA', 'status': 'Failure', 'errorCode': None}

    """
    # print(capcha, id)
    headers = {"Content-Type": "application/json", "x-request-id": str(uuid.uuid4()),
               "appid": "MYAADHAAR", "Accept-Language": "en_in"}
    otp_url = "https://stage1.uidai.gov.in/unifiedAppAuthService/api/v2/generate/aadhaar/otp"
    txnId = str(uuid.uuid4())
    data = {
        "uidNumber": uid,
        "captchaTxnId": id,
        "captchaValue": capcha,
        "transactionId": f"MYAADHAAR:{txnId}"
    }
    response = requests.post(otp_url, data=json.dumps(data),
                             headers=headers, verify=True)
    # global otpTxnNumber
    print(response.json())
    if(response.json()['status'] == "Success"):
        otpTxnNumber = (response.json())['txnId']
        return JsonResponse({'message': otpTxnNumber, 'status': "Success"})
    elif (response.json()['status'] == "Failure"):
        print("helo")
        return JsonResponse({'message': (response.json())["message"], 'status': "Failure"})
    # try:
    #     otpTxnNumber = (response.json())['txnId']
    # except:
    #     raise Exception("Invalid Captcha")
    # return HttpResponse((response.json())["txnId"])


def eKYC(request, otp, id, uid):
    # otp = input("o? ")
    ekyc_url = "https://stage1.uidai.gov.in/eAadhaarService/api/downloadOfflineEkyc"
    headers = {
        "Content-Type": "application/json", "X-Request-ID": str(uuid.uuid4()), "appID": "PORTAL", "transactionId": str(uuid.uuid4())
    }
    data = {
        "aadhaarOrVidNumber": 0, "txnNumber": f"{id}", "shareCode": "1729", "otp": f"{otp}",
        "deviceId": None, "transactionId": None, "unifiedAppRequestTxnId": None, "uid": uid, "vid": None
    }

    res = requests.post(ekyc_url, data=json.dumps(data),
                        headers=headers, verify=True)

    # {'status': 400, 'errorCode': 'UES-VAL-002', 'errorDetails': {'messageEnglish': 'Invalid OTP! Please enter 6 digit OTP to proceed further.', 'messageLocal': 'Invalid OTP! Please enter 6 digit OTP to proceed further.'}, 'transactionId': '73374dc1-826e-4a7e-8912-cccbef63c344'}
# {'uidNumber': 999988636660, 'mobileNumber': 0, 'txnId': 'mAadhaar:71d0aed7-cbe8-4eed-b3f3-19cfdd710272', 'status': 'Success', 'message': 'OTP generation done successfully'}
    ################################ Unzipping xml data ################################
    if(res.json()['status'] == 'Success'):
        ekyc_bytes = base64.b64decode(res.json()['eKycXML'])
        passcode = b"1729"

        with open("ekyc.zip", "wb") as zip_file:
            zip_file.write(ekyc_bytes)
        with ZipFile("ekyc.zip") as f:
            f.extractall(pwd=passcode)

        prefixed = [filename for filename in os.listdir(
            '.') if filename.startswith("offlineaadhaar")]
        with open(prefixed[0]) as xml_file:
            data_dict = xmltodict.parse(xml_file.read())
        json_data = json.dumps(data_dict)
        json_data = json.loads(json_data)

        if(json_data):
            country = (json_data)[
                'OfflinePaperlessKyc']['UidData']['Poa']["@country"]
            district = (json_data)[
                'OfflinePaperlessKyc']['UidData']['Poa']["@dist"]
            landmark = (json_data)[
                'OfflinePaperlessKyc']['UidData']['Poa']["@landmark"]
            house = (json_data)[
                'OfflinePaperlessKyc']['UidData']['Poa']["@house"]
            loc = (json_data)['OfflinePaperlessKyc']['UidData']['Poa']["@loc"]
            pc = (json_data)['OfflinePaperlessKyc']['UidData']['Poa']["@pc"]
            po = (json_data)['OfflinePaperlessKyc']['UidData']['Poa']["@po"]
            state = (json_data)[
                'OfflinePaperlessKyc']['UidData']['Poa']["@state"]
            street = (json_data)[
                'OfflinePaperlessKyc']['UidData']['Poa']["@street"]
            subdistrict = (json_data)[
                'OfflinePaperlessKyc']['UidData']['Poa']["@subdist"]
            vtc = (json_data)['OfflinePaperlessKyc']['UidData']['Poa']["@vtc"]
            list = User.objects.all()
            exist = None
            for x in list:
                if(decrypt(x.username) == uid):
                    exist = x.id
                    break

            username = uid

            os.remove(prefixed[0])
            os.remove("ekyc.zip")
          # email = (json_data)['OfflinePaperlessKyc']['UidData']['@e']
          # phone = (json_data)['OfflinePaperlessKyc']['UidData']['@m']
          # lastModified = ""
            name = (json_data)[
                'OfflinePaperlessKyc']['UidData']['Poi']['@name']

            if (exist == None):
                address = Address.objects.create(
                    aadhar=encrypt(uid),
                    country=encrypt(country),
                    district=encrypt(district),
                    landmark=encrypt(landmark),
                    house=encrypt(house),
                    loc=encrypt(loc),
                    pc=encrypt(pc),
                    po=encrypt(po),
                    state=encrypt(state),
                    street=encrypt(street),
                    subdistrict=encrypt(subdistrict),
                    vtc=encrypt(vtc)
                )
                User.objects.create(
                    username=encrypt(username),
                    # email=email,
                    # phone=phone,
                    # lastModified=lastModified,
                    name=encrypt(name),
                    address=address
                )
            else:
                # print(exist)
                # print(Address.objects.get(
                #     id=(User.objects.get(id=exist).address.id)).country)
                Address.objects.filter(id=(User.objects.get(id=exist).address.id)).update(
                    aadhar=encrypt(uid),
                    country=encrypt(country),
                    district=encrypt(district),
                    landmark=encrypt(landmark),
                    house=encrypt(house),
                    loc=encrypt(loc),
                    pc=encrypt(pc),
                    po=encrypt(po),
                    state=encrypt(state),
                    street=encrypt(street),
                    subdistrict=encrypt(subdistrict),
                    vtc=encrypt(vtc)
                )
                address = Address.objects.get(
                    id=(User.objects.get(id=exist).address.id))
                User.objects.filter(id=exist).update(
                    username=encrypt(username),
                    # email=email,
                    # phone=phone,
                    # lastModified=lastModified,
                    name=encrypt(name),
                    address=address
                )
        if(exist == None):
            users = User.objects.all()
            token = Token.objects.get(user=users[users.count()-1])
            thisUser = users[users.count()-1].id
        else:
            token = Token.objects.get(user=User.objects.get(id=exist))
            thisUser = exist
        return JsonResponse({"message": token.key, "id": thisUser, 'status': "Success"})
    else:
        return JsonResponse({"message": res.json()['errorDetails']['messageEnglish'], "status": "Fail"})


def createUser(request, uid):
    list = User.objects.all()
    exist = None
    for x in list:
        if(decrypt(x.username) == uid):
            exist = x.id
            break

    username = uid
    address = None
    if (exist == None):
        address = Address.objects.create(
            aadhar=encrypt(uid),
            country=encrypt("N.A."),
            district=encrypt("N.A."),
            landmark=encrypt("N.A."),
            house=encrypt("N.A."),
            loc=encrypt("N.A."),
            pc=encrypt("N.A."),
            po=encrypt("N.A."),
            state=encrypt("N.A."),
            street=encrypt("N.A."),
            subdistrict=encrypt("N.A."),
            vtc=encrypt("N.A.")
        )
        User.objects.create(
            username=encrypt(username),
            # email=email,
            # phone=phone,
            # lastModified=lastModified,
            name=encrypt("N.A."),
            address=address
        )
    if (exist == None):
        return HttpResponse(list[list.count()-1].id)
    else:
        return HttpResponse(exist)


def sentRequest(request, clientId, introducerId):
    users = Request_Sent.objects.filter(client=User.objects.get(id=clientId))
    already = False
    for user in users:
        already
        if user.status == 'empty':
            already = True
            break

    if(not already):
        Request_Sent.objects.create(
            client=User.objects.get(id=int(clientId)),
            introducer=User.objects.get(id=int(introducerId)),
        )

        return HttpResponse("Your Request has been sent!!")
    else:
        return HttpResponse("You have sent one request already!!")


def geoLocation(request, loc, po, pin, city, lat, lng):
    loc = loc
    city = city
    lat_gps = lat
    lng_gps = lng
    pincode_address = pin
    cordinate_gps = lat_gps+" , "+lng_gps
    postoffice = po
    client = User.objects.get(id=request.user.id)
    reqID = Request_Confirm.objects.filter(client=client)
    print(reqID)
    address = reqID[0].addressAttempt
    if(address < 5):
        if(loc != ""):
            # return HttpResponse("hi")
            address = loc+" , "+city

            data = requests.get('https://api.opencagedata.com/geocode/v1/json?q=' +
                                address+'&key=3a8206377b6e4887bcbc6b1d35120045')
            data = data.json()

            lat = str(data['results'][0]['geometry']['lat'])
            lng = str(data['results'][0]['geometry']['lng'])
            # return(HttpResponse(lat))
            cordinate_address = lat + ' , ' + lng
            distance = geodesic(cordinate_gps, cordinate_address).km
            distance = distance
            # return HttpResponse(request.user.id)
            client = User.objects.get(id=request.user.id)
            reqID = Request_Confirm.objects.filter(client=client)
            print(distance)
            address = reqID[0].addressAttempt
            print(address)

            if(distance < 5):
                reqID = reqID.update(addressAttempt=(address+1))
                return HttpResponse("sucess")
            elif(distance < 10):
                reqID = reqID.update(addressAttempt=(address+1))
                cord = lat_gps+"%2C"+lng_gps
                data = requests.get(
                    'https://api.opencagedata.com/geocode/v1/json?q='+cord+'&key=3a8206377b6e4887bcbc6b1d35120045')
                data = data.json()
                pincode_gps = str(data['results'][0]['components']['postcode'])
                if(pincode_address == pincode_gps):
                    return HttpResponse("sucess with warning")
                else:
                    return HttpResponse('faliure')
            else:
                return HttpResponse("failed1")

        elif(postoffice != ""):
            address = postoffice+" , "+city

            data = requests.get('https://api.opencagedata.com/geocode/v1/json?q=' +
                                address+'&key=3a8206377b6e4887bcbc6b1d35120045')
            data = data.json()

            lat = str(data['results'][0]['geometry']['lat'])
            lng = str(data['results'][0]['geometry']['lng'])

            cordinate_address = lat + ' , ' + lng
            distance = geodesic(cordinate_gps, cordinate_address).km
            distance = distance
            client = User.objects.get(id=request.user.id)
            reqID = Request_Confirm.objects.filter(client=client)
            print(distance)
            address = reqID[0].addressAttempt

            if(distance < 5):
                return HttpResponse("sucess")
            elif(distance < 10):
                cord = lat_gps+"%2C"+lng_gps
                data = requests.get(
                    'https://api.opencagedata.com/geocode/v1/json?q='+cord+'&key=3a8206377b6e4887bcbc6b1d35120045')
                data = data.json()
                pincode_gps = str(data['results'][0]['components']['postcode'])
                if(pincode_address == pincode_gps):
                    return HttpResponse("sucess with warning")
                else:
                    return HttpResponse('faliure')
            else:
                reqID = reqID.update(addressAttempt=(address+1))
                return HttpResponse("failed2")

        else:
            client = User.objects.get(id=request.user.id)
            reqID = Request_Confirm.objects.filter(client=client)
            address = reqID[0].addressAttempt
            reqID = reqID.update(addressAttempt=(address+1))
            return HttpResponse("adress not qualified")
    else:
        return HttpResponse("adress exceed")
