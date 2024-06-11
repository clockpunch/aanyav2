import requests
from fake_useragent import UserAgent
import json
import datetime
import holidays

ua = UserAgent()

session = requests.session()

ph_holidays = holidays.PH()

if datetime.datetime.today() in ph_holidays:
    # Today is a holiday Labor Day 2023-05-09 12:59
    print('Today is a holiday', ph_holidays.get(datetime.datetime.today().isoformat()), datetime.datetime.today().strftime('%Y-%m-%d %I:%M'))
else:
    headers1 = {
        'Host': 'appv2.aanyahr.com:8000',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Sec-Ch-Ua-Mobile': '?0',
        'Authorization': 'Bearer null',
        'User-Agent': ua.google,
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Origin': 'https://appv2.aanyahr.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://appv2.aanyahr.com/',
        'Accept-Language': 'en-US,en;q=0.9',
        'Priority': 'u=1, i',
    }

    json_data1 = {
        # set username
        'username': '',
        'password': '',
        # set company code
        'companyCode': '',
        'remember': True,
        # set ip
        'ip1': '',
        'ip2': '',
        'device': 'Windows',
        'browser': 'Chrome',
    }

    response1 = requests.post(
        'https://appv2.aanyahr.com:8000/api/user/authenticateLogin',
        headers=headers1,
        json=json_data1,
        timeout=60
    )

    response1_json = response1.json()

    headers2 = {
        # set ip
        'Ip1': '',
        'Ip2': '',
        'Host': 'appv2.aanyahr.com:8000',
        'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'Authorization': 'Bearer ' + response1_json['payload']['token'],
        # set user
        'User': '',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': ua.google,
        'Access-Control-Max-Age': '86400',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://appv2.aanyahr.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://appv2.aanyahr.com/',
        'Accept-Language': 'en-US,en;q=0.9',
        'Priority': 'u=1, i',
        # removed base64 string with encryption
        'Browser': '',
        'Series': '',
        'Device': '',
        'Accesslevel': '',
        'Loginid': '',
    }

    # 'bundy': 0,
    # clock in = 0
    # clock out = 1
    json_data2 = {
        'bundy': 0,
        'bundyType': 0,
    }

    response2 = requests.post('https://appv2.aanyahr.com:8000/api/attendance/postBundy', headers=headers2, json=json_data2)

    if response2.status_code == 200:
        response2_json = response2.json()
        if response2_json.get("message") == "Successful Clock In.":
            print('Clocked In on', datetime.datetime.now().strftime('%a, %b %d, %Y at %H:%M:%S'))
        else:
            print("Clock In was not successful.", datetime.datetime.now().strftime('%a, %b %d, %Y at %H:%M:%S'))
    else:
        print("Request failed with status code:", datetime.datetime.now().strftime('%a, %b %d, %Y at %H:%M:%S'), response2.status_code)