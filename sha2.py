import hashlib
import requests
import re

url = "https://ringzer0ctf.com/login"
url_res = "https://ringzer0ctf.com/challenges/57/"
payload = {'username': 'xxx', 'password': 'xxx'}
hash_regex = "-----BEGINHASH-----<br\/>(\w+)"
salt_regex = "-----BEGINSALT-----<br\/>(\w+)"
flag = "FLAG-\w+"

session = requests.Session()

session.post(url, data=payload)
contents = session.get(url_res)

message = re.sub(r'\s+', '', contents.text)

sha1 = re.search(hash_regex,message)
sha1 = sha1.group(1)

salt = re.search(salt_regex,message)
salt = salt.group(1)

print("sha1: "+sha1)
print("salt: "+salt)


for i in range(0,9999):
    num = str(i).encode('utf-8')
    encoded1 = hashlib.sha1(salt+num).hexdigest()
    encoded2 = hashlib.sha1(num+salt).hexdigest()
    if(encoded1==sha1 or encoded2==sha1):
        trovato = i
        print("Cracked: " + num)
        break

url_res = url_res + str(trovato)
response = session.post(url_res)

flg = re.search(flag,response.text)
print(flg.group())
