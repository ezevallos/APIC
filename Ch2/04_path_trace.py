"""
Path Trace Student Work File
APIC-EM Workshop
October 15, 2017
"""
#==================================================
# Section 1. Setup the environment and variables required to interact with the APIC-EM
#===================================================
#+++++++++++Add Values+++++++++++++++
#import functions
import requests
import json
import time
import sys
from my_apic_em_functions import *
from tabulate import *

#disable SSL certificate warnings
requests.packages.urllib3.disable_warnings()

#++++++++++++++++++++++++++++++++++++


#+++++++++++Add Values+++++++++++++++
# Path Trace API URL for flow_analysis endpoint
api_url = "https://devnetsbx-netacad-apicem-1.cisco.com/api/v1/flow-analysis"
# Get service ticket number using imported function
ticket = get_ticket()
# Create headers for requests to the API
headers = {
    "Content-Type": "application/json",
    "X-Auth-Token": ticket
}
#++++++++++++++++++++++++++++++++++++

#============================
# Section 2. Display list of devices and IPs by calling get_host() and get_devices()
#============================

#+++++++++++Add Values+++++++++++++++
print("List of hosts on the network: \n")
print_hosts()
print("List of devices on the network: \n")
print_devices()
#++++++++++++++++++++++++++++++++++++

print('\n\n') #prints two blank lines to format output

# ============================
# Section 3. Get the source and destination IP addresses for the Path Trace
# ============================

while True:
    #+++++++++++Add Values+++++++++++++++
    s_ip = input("Please enter the source host IP address for the path trace: ")
    d_ip = input("Please enter the destination host IP address for the path trace: ")
    #++++++++++++++++++++++++++++++++++++
    #Various error traps should be completed here - POSSIBLE CHALLENGE

    if s_ip != '' or d_ip != '':
        #this creates a python dictionary that will be converted to a JSON object and posted
        path_data = {
                    "sourceIP": s_ip, 
                    "destIP": d_ip
                    }
        # Challenge:
        print("Source IP address is: ", path_data["sourceIP"])
        print("Destination IP address is: ", path_data["destIP"])
        break  #Exit loop if values supplied
    else:
        print("\n\nYOU MUST ENTER IP ADDRESSES TO CONTINUE.\nUSE CTRL-C TO QUIT\n")
        continue  #Return to beginning of loop and repeat

#============================
# Section 4. Initiate the Path Trace and get the flowAnalysisId
#============================

#+++++++++++Add Values+++++++++++++++    
# Post request to initiate Path Trace
path =  json.dumps(path_data)
resp =  requests.post(api_url, path, headers=headers, verify=False)

# Inspect the return, get the Flow Analysis ID, put it into a variable
resp_json = resp.json()
flowAnalysisId =  resp_json["response"]["flowAnalysisId"]
print('FLOW ANALYSIS ID: ' + flowAnalysisId)

#============================
# Section 5. Check status of Path Trace request, output results when COMPLETED
#============================


#initialize variable to hold the status of the path trace
status = ""

#+++++++++++Add Values+++++++++++++++
#Add Flow Analysis ID to the endpoint URL in order to check the status of this specific path trace
check_url = api_url + "/" + flowAnalysisId
#++++++++++++++++++++++++++++++++++++

checks = 1 #variable to increment within the while loop. Will trigger exit from loop after x iterations

while status != 'COMPLETED':
    
    r = requests.get(check_url,headers=headers,params="",verify = False)
    response_json = r.json()
    #+++++++++++Add Values+++++++++++++++
    status = response_json["response"]["request"]["status"]
    #++++++++++++++++++++++++++++++++++++
    print('REQUEST STATUS: ' + status) #Print the status as the loop runs
    #wait one second before trying again
    time.sleep(1)
    if checks == 15: #number of iterations before exit of loop; change depending on conditions
        print("Number of status checks exceeds limit. Possible problem with Path Trace.")
        #break
        sys.exit()
    elif status == 'FAILED':
        print('Problem with Path Trace')
        #break
        sys.exit()
    checks += 1
        

#============================
# Section 6. Display results
#============================

# Create required variables
#+++++++++++Add Values+++++++++++++++
path_source = response_json["response"]["request"]["sourceIP"]
path_dest = response_json["response"]["request"]["destIP"]
networkElementsInfo = response_json["response"]["networkElementsInfo"]
#+++++++++++++++++++++++++++++++++++++

all_devices = []     # A list variable to store the hosts and devices
device_no = 1 #this variable is an ordinal number for each device, incremented in the loop

#Iterate through returned Path Trace JSON and populate list of path information
for networkElement in networkElementsInfo:
    # test if the devices DOES NOT have a "name", absence of "name" identifies an end host
    if not 'name' in networkElement:  #assigns values to the variables for the hosts
       name = 'Unamed Host'
       ip = networkElement['ip']
       egressInterfaceName = 'UNKNOWN'
       ingressInterfaceName = 'UNKNOWN'
       device = [device_no,name,ip,ingressInterfaceName,egressInterfaceName]
    # if there is the "name" key, then it is an intermediary device
    else: #assigns values to the variables for the intermediary devices
       name = networkElement['name']
       ip = networkElement['ip']   
       if 'egressInterface' in networkElement: #not all intermediary devices have ingress and egress interfaces
           egressInterfaceName = networkElement['egressInterface']['physicalInterface']['name']
       else:
           egressInterfaceName = 'UNKNOWN'
           
       if 'ingressInterface' in networkElement:
           ingressInterfaceName = networkElement['ingressInterface']['physicalInterface']['name']
       else:
           ingressInterfaceName = 'UNKNOWN'       
       device = [device_no,name,ip,ingressInterfaceName,egressInterfaceName] #create the list of info to be displayed
    all_devices.append(device) #add this list of info for the device as a new line in this variable
    device_no += 1  #increments the ordinal variable for the device in the list

print('Path trace: \n Source: ' + path_source + '\n\tDestination: ' + path_dest) #print the source and destination IPs for the trace
print('List of devices on path:')
print (tabulate(all_devices,headers=['Item','Name','IP','Ingress Int','Egress Int'],tablefmt="rst")) #print the table of devices in the path trace
