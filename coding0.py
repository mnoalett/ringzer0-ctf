import cookielib
import urllib
import urllib2
from bs4 import BeautifulSoup
import hashlib
import requests
import re

url = "https://ringzer0ctf.com/login"
url_res = "https://ringzer0ctf.com/challenges/13/"
payload = {'username': 'xxx', 'password': 'xxx'}
msg = "-----BEGINMESSAGE-----(\w+)"
flag = "FLAG-\w+"

session = requests.Session()

session.post(url, data=payload)
contents = session.get(url_res)

soup = BeautifulSoup(contents.text,"html.parser")
message = soup.find("div", {"class": "message"})
message = message.text
message = re.sub(r'\s+', '', message)
message = re.search(msg,message)
message = message.group(1)

encoded = hashlib.sha512(message).hexdigest()

url_res = url_res + encoded
response = session.post(url_res)

flg = re.search(flag,response.text)
print flg.group()
