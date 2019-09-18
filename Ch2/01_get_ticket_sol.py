"""
01_get_ticket.py
This script retrieves an authentication token from APIC-EM and prints out its value
It is standalone, there is no dependency.
MBenson
11/12/2017
"""
import json       # Import JSON encoder and decoder module
import requests   # requests module used to send REST requests to API

requests.packages.urllib3.disable_warnings()  # Disable SSL warnings

# TICKET API URL
#api_url = "https://{YOUR-APICEM}.cisco.com/api/v1/ticket"
api_url = "https://sandboxapicem.cisco.com/api/v1/ticket" # change this if using a different APIC-EM sandbox


# All APIC-EM REST API request and response content type is JSON.
headers = {
    "content-type": "application/json"
}

# JSON  input body content
#body_json = {
#    "username": "!!!REPLACE ME with the Username for {YOUR-APICEM}.cisco.com!!!",
#    "password": "!!!REPLACE ME with the Password for {YOUR-APICEM}.cisco.com!!!"
#}
body_json = {
    "username": "devnetuser",     # change this if using a different APIC-EM sandbox
    "password": "Cisco123!"       # change this if using a different APIC-EM sandbox
}


# Make request and get response - "resp" is the response of this request
resp = requests.post(api_url, json.dumps(body_json), headers=headers, verify=False)

# Create object to contain the request status
print("Ticket request status: ", resp.status_code)  # display response code

# Create object to contain the converted json-formatted response
response_json = resp.json()

# parse data for service ticket
serviceTicket = response_json["response"]["serviceTicket"]

# display service ticket value
print("The service ticket number is: ", serviceTicket)
