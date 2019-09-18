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
!!!REPLACEME!!!

# disable SSL certificate warnings
!!!REPLACEME!!!

#++++++++++++++++++++++++++++++++++++


#+++++++++++Add Values+++++++++++++++
# Path Trace API URL for flow_analysis endpoint
api_url = !!!REPLACEME!!!   # URL of API endpoint
# Get service ticket number using imported function
ticket = !!!REPLACEME!!!     # Call your function name that returns the service ticket
# Create headers for requests to the API
headers = !!!REPLACEME!!!    # Create dictionary containing headers for the request with "content-type" and "X-Auth-Token"
#++++++++++++++++++++++++++++++++++++

#============================
# Section 2. Display list of devices and IPs by calling get_host() and get_devices()
#============================

#+++++++++++Add Values+++++++++++++++
# display message identifying what is to be printed on the next line
print(!!!REPLACEME!!!)
# Call your function name that displays hosts
!!!REPLACEME!!!
# Display message identifying what is to be printed
print(!!!REPLACEME!!!)
# Call your function name that displays network devices
!!!REPLACEME!!!
#++++++++++++++++++++++++++++++++++++

print("\n\n")  # prints two blank lines to format output

# ============================
# Section 3. Get the source and destination IP addresses for the Path Trace
# ============================

while True:
    #+++++++++++Add Values+++++++++++++++
    # Request user input for source IP address, e.g. "Please enter the source
    # IP address"
    s_ip = !!!REPLACEME!!!  # Request user input for source host IP address, e.g. "Please enter the source host IP address"
    d_ip = !!!REPLACEME!!!  # Request user input for destination host IP address, e.g. "Please enter the destination host IP address"
    #++++++++++++++++++++++++++++++++++++
    # Various error traps could be completed here - POSSIBLE CHALLENGE

    if s_ip != "" or d_ip != "":
        # this creates a python dictionary that will be converted to a JSON
        # object and posted
        path_data = {
            "sourceIP": s_ip,
            "destIP": d_ip
        }
        # Optional: Add statements that display the source and destination IP
        # addresses that will be used. And asks user to verify. Loop if not
        # verified by user.
        break  # Exit loop if values supplied
    else:
        print("\n\nYOU MUST ENTER IP ADDRESSES TO CONTINUE.\nUSE CTRL-C TO QUIT\n")
        continue  # Return to beginning of loop and repeat

#============================
# Section 4. Initiate the Path Trace and get the flowAnalysisId
#============================

#+++++++++++Add Values+++++++++++++++
# Post request to initiate Path Trace
# Convert the path_data dictionary into JSON for use in the request using json.dumps()
path = !!!REPLACEME!!!
# Make the request. Construct the post request to the API
resp = requests.post(!!!REPLACEME!!!, !!!REPLACEME!!!, headers=headers, verify=False)

# Inspect the return, get the Flow Analysis ID, put it into a variable
resp_json = resp.json()
flowAnalysisId = resp_json["response"][!!!REPLACEME!!!]
print("FLOW ANALYSIS ID: ", flowAnalysisId)

#============================
# Section 5. Check status of Path Trace request, output results when COMPLETED
#============================

#+++++++++++Add Values+++++++++++++++
# Add Flow Analysis ID to the endpoint URL in order to check the status of
# this specific path trace (e.g. https://a.b.c.d/api/v1/flow-analysis/2a014833-a99f-4067-8461-5dff58b2e1f2)
check_url = api_url + "/" + !!!REPLACEME!!!
#++++++++++++++++++++++++++++++++++++

# initialize variable to hold the status of the path trace
status = ""
checks = 1  # variable to increment within the while loop. Will trigger exit from loop after x iterations
while status != "COMPLETED":
    r = requests.get(check_url, headers=headers, verify=False)
    response_json = r.json()
    #+++++++++++Add Values+++++++++++++++
    status = response_json["response"]["request"][!!!REPLACEME!!!] # Assign the value of the status of the path trace request from response_json
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

# Create required variables
#+++++++++++Add Values+++++++++++++++
# the source address for the trace, printed below
path_source = response_json["response"]["request"]["sourceIP"]
# the destination address for the trace, printed below
path_dest = response_json["response"][!!!REPLACEME!!!][!!!REPLACEME!!!]
# Assign the list of all network element dictionaries from response_json
networkElementsInfo = response_json["response"][!!!REPLACEME!!!]
#+++++++++++++++++++++++++++++++++++++

all_devices = []     # A list variable to store the hosts and devices
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
