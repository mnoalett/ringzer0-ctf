from bs4 import BeautifulSoup
import hashlib
import requests
import re

url = "https://ringzer0ctf.com/login"
url_res = "https://ringzer0ctf.com/challenges/14/"
payload = {'username': 'xxx', 'password': 'xxx'}
msg = "-----BEGINMESSAGE-----(\w+)"
flag = "FLAG-\w+"

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

session = requests.Session()

session.post(url, data=payload)
contents = session.get(url_res)

soup = BeautifulSoup(contents.text,"html.parser")
message = soup.find("div", {"class": "message"})
message = message.text
message = re.sub(r'\s+', '', message)
message = re.search(msg,message)
message = message.group(1)

message = text_from_bits(message)

message = message.encode('utf-8')

encoded = hashlib.sha512(message).hexdigest()

url_res = url_res + encoded
response = session.post(url_res)

flg = re.search(flag,response.text)
print(flg.group())
