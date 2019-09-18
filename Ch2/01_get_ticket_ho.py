import json
import requests
requests.packages.urllib3.disable_warnings()

api_url = "https://devnetsbx-netacad-apicem-1.cisco.com/api/v1/ticket"
headers = {
    "content-type": "application/json"
}
body_json = {
    "username": "devnetuser",
    "password": "NTgmY5UY"
}

resp=requests.post(api_url,json.dumps(body_json),headers=headers,verify=False)

print("Ticket request status: ", resp.status_code)

response_json = resp.json()
serviceTicket = response_json["response"]["serviceTicket"]
print("The service ticket number is: ", serviceTicket)