import json
import os
import requests
from server.RgbMatrix import RgbMatrix
import time

print("Starting...")

#faboi_url = 'https://faboinet.herokuapp.com'
faboi_url = 'https://192.168.1.67:8000'

pid = os.fork()
if pid <= 0:
    # CHILD
    os.system("./ngrok http 5000")
    while True:
        time.sleep(1)
        try:
            os.kill(os.getppid(), 0)
        except OSError:
            print("Killing the child...")
            exit();

# PARENT
# @TODO: Improve this so we don't rely on time.sleep()
time.sleep(3)
print("Looking for the ngrok route...")
os.system("curl http://localhost:4040/api/tunnels > tunnels.json")

print("Creating temporary tunnels.json...")
with open('tunnels.json') as f:
    tunnels = json.load(f)

public_urls = []
for i in tunnels['tunnels']:
    public_urls.append(i['public_url'])
    if 'https' in i['public_url']:
        break

print("Public URLs:")
print(public_urls)

if os.path.exists("tunnels.json"):
    os.remove("tunnels.json")
print("\nRemoved tunnels.json.")

url = public_urls[-1]

post_data = {'action': "create", 'url': url}
headers = {'Referer': url}
pi_connect = faboi_url + '/apps/pixeled/pi_connect'
response = requests.post(pi_connect, json=post_data, headers=headers)
print(response)
print(response.content)
data = response.json()
print("RESPONSE DATA:", data)
# @TODO First confirm it's code 200...
if data['success']:
    if 'code' not in data:
        print("INVALID RESPONSE DATA")
        print(data)
        print("EXITING....")
        exit(0)

    code = data['code']
    code_json = {'code': code, 'connected': False}

    with open("pixeled_connection", "w") as f:
        json.dump(code_json, f)

    post_data2 = {"action": 'confirm', 'success': True, 'code': code}
    response2 = requests.post(pi_connect, json=post_data2, headers=headers)
    data2 = response2.json()
    if 'success' in data2 and data2['success']:
        print("SUCCESS")
    else:
        print("HORRIBLE FAILURE!!", data2)
