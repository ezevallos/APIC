"""
Path Trace Solution
APIC-EM Workshop
October 15, 2017
"""
#==================================================
# Section 1. Setup the environment and variables required to interact with the APIC-EM
#===================================================
import requests
import json
import time
from apic_em_functions_sol import *
from tabulate import *

# disables certificate security warning
requests.packages.urllib3.disable_warnings()

#++++++++++++++++++++++++++++++++++++++++
# Path Trace API URL for flow_analysis endpoint
#api_url = "https://{YOUR-APICEM}.cisco.com/api/v1/flow-analysis"
api_url = "https://SandBoxAPICEM.cisco.com/api/v1/flow-analysis"  # change this if using a different APIC-EM sandbox

# Get service ticket number using imported function
ticket = get_ticket()
# Create headers for requests to the API
headers = {
    "content-type": "application/json",
    "X-Auth-Token": ticket
}
#++++++++++++++++++++++++++++++++++++++++++

#============================
# Section 2. Display list of devices and IPs by calling get_host() and get_devices()
#============================

#++++++++++++++++++++++++++++++++++++++++++
print("List of hosts on the network: ")
print_hosts()
print("List of devices on the network: ")
print_devices()
#++++++++++++++++++++++++++++++++++++++++++

print("\n\n")  # prints two blank lines to format output

# ============================
# Section 3. Get the source and destination IP addresses for the Path Trace
# ============================

while True:
    #++++++++++++++++++++++++++++++++++++++++++
    s_ip = input("Please enter the source host IP address for the path trace: ")
    d_ip = input("Please enter the destination host IP address for the path trace: ")
    #++++++++++++++++++++++++++++++++++++++++++
    # Various error traps could be completed here - POSSIBLE CHALLENGE
    if s_ip != "" or d_ip != "":
        # this creates a python dictionary that will be dumped as a
        path_data = {
            "sourceIP": s_ip,
            "destIP": d_ip
        }
        # stud: optional challenge
        print("Source IP address is: ",       path_data["sourceIP"])
        print("Destination IP address is: ",  path_data["destIP"])  # stud: optional challenge
        break  # Exit loop if values supplied
    else:
        print("\n\nYOU MUST ENTER IP ADDRESSES TO CONTINUE.\nUSE CTRL-C TO QUIT\n")
        continue  # Return to beginning of loop and repeat

#============================
# Section 4. Initiate the Path Trace and get the flowAnalysisId
#============================

#++++++++++++++++++++++++++++++++++++
# Post request to initiate Path Trace
# Convert the path_data dictionary into JSON for use in the request using json.dumps()
path = json.dumps(path_data)
# Make the request. Construct the post request to the API
resp = requests.post(api_url, path, headers=headers, verify=False)

# Inspect the return, get the Flow Analysis ID, put it into a variable
resp_json = resp.json()
flowAnalysisId = resp_json["response"]["flowAnalysisId"]
print("FLOW ANALYSIS ID: ", flowAnalysisId)
#++++++++++++++++++++++++++++++++++++

#============================
# Section 5. Check status of Path Trace request, output results when COMPLETED
#============================

# Add Flow Analysis ID to URL in order to check the status of this specific path trace
# this specific path trace (e.g. https://a.b.c.d/api/v1/flow-analysis/2a014833-a99f-4067-8461-5dff58b2e1f2)
#++++++++++++++++++++++++++++++++++++
check_url = api_url + "/" + flowAnalysisId
#++++++++++++++++++++++++++++++++++++

# initialize variable to hold the status of the path trace
status = ""
checks = 1  # variable to increment within the while loop. Will trigger exit from loop after x iterations
while status != "COMPLETED":
    r = requests.get(check_url, headers=headers, verify=False)
    response_json = r.json()
    #++++++++++++++++++++++++++++++++++++
    status = response_json["response"]["request"]["status"]
    #++++++++++++++++++++++++++++++++++++
    print("REQUEST STATUS: ", status)  # Print the status as the loop runs
    # wait one second before trying again
    time.sleep(1)
    if checks == 15:  # number of iterations before exit of loop; change depending on conditions
        # break the execution
        raise Exception("Number of status checks exceeds limit. Possible problem with Path Trace.!")
    elif status == "FAILED":
        # break the execution
        raise Exception("Problem with Path Trace - FAILED!")
    checks += 1


#============================
# Section 6. Display results
#============================

#+++++++++++Add Values+++++++++++++++
# Create required variables
# the source address for the trace, printed below
path_source = response_json["response"]["request"]["sourceIP"]
# the destination address for the trace, printed below
path_dest = response_json["response"]["request"]["destIP"]
# variable holding a list of all the network element dictionaries
networkElementsInfo = response_json["response"]["networkElementsInfo"]
#++++++++++++++++++++++++++++++++++++

all_devices = []  # create a list variable to store the hosts and devices
device_no = 1  # this variable is an ordinal number for each device, incremented in the loop
# Iterate through returned Path Trace JSON and populate list of path
# information
for networkElement in networkElementsInfo:
    # test if the devices DOES NOT have a "name", absence of "name" identifies
    # an end host
    if "name" not in networkElement:  # assigns values to the variables for the hosts
        name = "Unnamed Host"
        ip = networkElement["ip"]
        egressInterfaceName = "UNKNOWN"
        ingressInterfaceName = "UNKNOWN"
    # if there is the "name" key, then it is an intermediary device
    else:  # assigns values to the variables for the intermediary devices
        name = networkElement["name"]
        ip = networkElement["ip"]
        if "egressInterface" in networkElement:  # not all intermediary devices have ingress and egress interfaces
            egressInterfaceName = networkElement["egressInterface"]["physicalInterface"]["name"]
        else:
            egressInterfaceName = "UNKNOWN"

        if "ingressInterface" in networkElement:
            ingressInterfaceName = networkElement["ingressInterface"]["physicalInterface"]["name"]
        else:
            ingressInterfaceName = "UNKNOWN"
    
    # create the list of info to be displayed
    device = [
                device_no,
                name,
                ip,
                ingressInterfaceName,
                egressInterfaceName
             ]
    # add this list of info for the device as a new line in this variable
    all_devices.append(device)
    device_no += 1  # increments the ordinal variable for the device in the list

# print the source and destination IPs for the trace
print("Path trace: \n Source: ", path_source, "\n Destination: ", path_dest)  
# print the table of devices in the path trace
print("List of devices on path:")
table_header = [
                "Item",
                "Name",
                "IP",
                "Ingress Int",
                "Egress Int"
               ]
print( tabulate(all_devices, table_header) )  
