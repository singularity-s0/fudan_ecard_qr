# The purpose of this script is to get the content of QR Code from Fudan Servers
# It receives the UIS username and password from input and outputs the QR content
#
# Script modified from https://github.com/syang-ng/FudanDaily (took the UIS login part)
# Thanks to the original author

import json
import requests
import pyqrcode
from bs4 import BeautifulSoup

headers = {
    "Origin": "https://ecard.fudan.edu.cn",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1",
    "Referer": "https://ecard.fudan.edu.cn"
}

data = {
    "username": "", #UIS ID
    "password": "" #UIS Password
}

login_url = "https://uis.fudan.edu.cn/authserver/login?service=https%3A%2F%2Fworkflow1.fudan.edu.cn%2Fsite%2Flogin%2Fcas-login%3Fredirect_url%3Dhttps%253A%252F%252Fworkflow1.fudan.edu.cn%252Fopen%252Fconnection%252Findex%253Fapp_id%253Dc5gI0Ro%2526state%253D%2526redirect_url%253Dhttps%253A%252F%252Fecard.fudan.edu.cn%252Fepay%252Fwxpage%252Ffudan%252Fzfm%252Fqrcode%253Furl%253D0"
get_qr_url = "https://ecard.fudan.edu.cn/epay/wxpage/fudan/zfm/qrcode"
s = requests.Session()
response = s.get(login_url)
content = response.text
soup = BeautifulSoup(content, "lxml")
inputs = soup.find_all("input")
for i in inputs[2::]:
    data[i.get("name")] = i.get("value")
response = s.post(login_url, data=data)

response = s.get(get_qr_url)
soup = BeautifulSoup(response.text, "lxml")
qr = soup.find_all("input", id="myText")

for i in qr:
    text = pyqrcode.create(i['value'])
    print(text.terminal())
