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


captcha_url = "https://stage1.uidai.gov.in/unifiedAppAuthService/api/v2/get/captcha"
otp_url = "https://stage1.uidai.gov.in/unifiedAppAuthService/api/v2/generate/aadhaar/otp"
ekyc_url = "https://stage1.uidai.gov.in/eAadhaarService/api/downloadOfflineEkyc"
passcode = b"1729"
############ Captcha Fetch #################################
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
out = base64.b64decode(base64_str)
savepath = os.path.join('./captcha.png')
img = Image.open(io.BytesIO(out))
img.save(savepath)
captcha = input("captcha? ")
uidNumber = input("uid? ")
###################### OTP Generation #######################
headers = {"Content-Type": "application/json", "x-request-id": str(uuid.uuid4()),
           "appid": "MYAADHAAR", "Accept-Language": "en_in"}
txnId = str(uuid.uuid4())
data = {
    "uidNumber": uidNumber,
    "captchaTxnId": res.json()['captchaTxnId'],
    "captchaValue": captcha,
    "transactionId": f"MYAADHAAR:{txnId}"
}
res = requests.post(otp_url, data=json.dumps(data),
                    headers=headers, verify=True)
print(res.json())
######################## eKYC xml base64 ################
otp = int(input("otp? "))
print("I am not printed", otp)
headers = {
    "Content-Type": "application/json", "X-Request-ID": str(uuid.uuid4()), "appID": "PORTAL", "transactionId": str(uuid.uuid4())
}
data = {
    "aadhaarOrVidNumber": 0, "txnNumber": f"{res.json()['txnId']}", "shareCode": "1729", "otp": f"{otp}",
    "deviceId": None, "transactionId": None, "unifiedAppRequestTxnId": None, "uid": uidNumber, "vid": None
}
print(data)

res = requests.post(ekyc_url, data=json.dumps(data),
                    headers=headers, verify=True)
# print(res.json())
################################ Unzipping xml data ################################
ekyc_bytes = base64.b64decode(res.json()['eKycXML'])
with open("ekyc.zip", "wb") as zip_file:
    zip_file.write(ekyc_bytes)
with ZipFile("ekyc.zip") as f:
    f.extractall(pwd=passcode)

prefixed = [filename for filename in os.listdir(
    '.') if filename.startswith("offlineaadhaar")]
with open(prefixed[0]) as xml_file:
    data_dict = xmltodict.parse(xml_file.read())
json_data = json.dumps(data_dict)
print(json_data)
os.remove(prefixed[0])
os.remove("captcha.png")
os.remove("ekyc.zip")
