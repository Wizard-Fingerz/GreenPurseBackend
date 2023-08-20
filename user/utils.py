import requests
from django.conf import settings
import requests


# def send_otp(phone_number, otp):
#     url = "https://wipple-sms-verify-otp.p.rapidapi.com/verify"

#     querystring = {"phone_number": phone_number,
#                    "verification_code": otp, "app_name": "greenpurseapp"}

#     headers = {
#         "X-RapidAPI-Key": "406a819f30msh819e65dae0d4faep1993fcjsnc5fb31f1754c",
#         "X-RapidAPI-Host": "wipple-sms-verify-otp.p.rapidapi.com"
#     }

#     response = requests.get(url, headers=headers, params=querystring)

#     print(response.json())
#     return bool(response.ok)
