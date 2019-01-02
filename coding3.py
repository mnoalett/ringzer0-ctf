from bs4 import BeautifulSoup
import hashlib
import requests
import re

url = "https://ringzer0ctf.com/login"
url_res = "https://ringzer0ctf.com/challenges/32/"
payload = {'username': 'xxx', 'password': 'xxx'}
msg = "-----BEGINMESSAGE-----(\d+\+\d+\w+\d+\-\d+)"
flag = "FLAG-\w+"
hexm = "0x[0-9a-fA-F]+" 

session = requests.Session()

session.post(url, data=payload)
contents = session.get(url_res)

soup = BeautifulSoup(contents.text,"html.parser")
message = soup.find("div", {"class": "message"})
message = message.text
message = re.sub(r'\s+', '', message)
message = re.search(msg,message)
message = message.group(1)
first = re.search("\d+",message).group()
second = re.search(hexm,message).group()
third = message.split('-')[1]

second = int(second,16)
third = int(third,2)

total = int(first)+int(second)-int(third)

url_res = url_res + str(total)
response = session.post(url_res)

flg = re.search(flag,response.text)
print(flg.group())
