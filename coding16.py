from bs4 import BeautifulSoup
import base64
import requests
from itertools import cycle, izip
import re

url = "https://ringzer0ctf.com/login"
url_res = "https://ringzer0ctf.com/challenges/16/"
payload = {'username': 'xxx', 'password': 'xxx'}
xor_key = "-----BEGINXORKEY-----(\w+)"
cheper_text = "-----BEGINCRYPTEDMESSAGE-----([^\] \b]*=)"
flag = "FLAG-\w+"

session = requests.Session()

session.post(url, data=payload)
contents = session.get(url_res)

soup = BeautifulSoup(contents.text,"html.parser")
html = soup.findAll("div", {"class": "message"})
hidden_xor_key = re.sub(r'\s+', '', html[0].text)
hidden_xor_key = re.search(xor_key,hidden_xor_key)
hidden_xor_key = hidden_xor_key.group(1)

message = re.sub(r'\s+', '', html[1].text)
message = re.search(cheper_text,message)
message = message.group(1)

key_len = 10

for i in range(0, len(hidden_xor_key)-key_len+1):
   enc_key = hidden_xor_key[i:i+key_len]
   ct = base64.b64decode(message)
   msg = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(ct, cycle(enc_key)))
   pattern = re.compile("^[a-zA-Z0-9_]*$")
   if pattern.match(msg):
      message = msg

url_res = url_res + message
response = session.post(url_res)

flg = re.search(flag,response.text)
print(flg.group())
