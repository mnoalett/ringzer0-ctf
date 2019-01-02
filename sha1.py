from bs4 import BeautifulSoup
import hashlib
import requests
import re

url = "https://ringzer0ctf.com/login"
url_res = "https://ringzer0ctf.com/challenges/56/"
payload = {'username': 'xxx', 'password': 'xxx'}
msg = "-----BEGINHASH-----(\w+)"
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

#print(message)

for i in range(0,9999):
    num = str(i).encode('utf-8')
    encoded = hashlib.sha1(num).hexdigest()
    if(encoded==message):
        trovato = i
        break

url_res = url_res + str(trovato)
response = session.post(url_res)

flg = re.search(flag,response.text)
print(flg.group())
