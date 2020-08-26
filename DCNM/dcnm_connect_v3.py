import os
import sys
import requests
import json
import getpass
import base64
from requests.auth import HTTPBasicAuth
from PyInquirer import prompt, print_json, style_from_dict, Token

# Disable Certificate warning
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

# Global variables
dcnm_hostname = "dcnm.checkpoint.com"

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

# Functions

def get_auth_token(dcnm_hostname=dcnm_hostname):
    """ Authenticates with controller and returns a token to be used in subsequent API invocations
    """
    username = input("Username:")
    password = getpass.getpass("Password:")
    
    # Print login message to terminal
    print("----------------------------------------------------")
    print("DCNM Login to {} as {} ...".format(dcnm_hostname, username))

    login_url = "https://{}/rest/logon".format(dcnm_hostname)
    payload = "{\"expirationTime\":10000000000}"

    authenStr="%s:%s" % (username, password)

    base64string = base64.encodebytes(bytes(authenStr, 'utf-8'))
    tmpstr= "Basic %s" % base64string
    authorizationStr = tmpstr.replace("b\'","").replace("\\n\'","")
    #print(authorizationStr)

    headers = {
      'content-type': "application/json",
      'authorization': authorizationStr,
      'cache-control': "no-cache"
      }

    result = requests.post(url=login_url, data=payload, headers=headers, verify=False)
    result.raise_for_status()

    token = result.json()["Dcnm-Token"]
    print("----------------------------------------------------")
    print("You have successfully logged in as {}.".format(username))
    print("----------------------------------------------------")
    return {
        "dcnm_hostname": dcnm_hostname,
        "token": token
    }


def create_url(path, dcnm_hostname=dcnm_hostname):
    """ Helper function to create a DCNM API endpoint URL
    """
    return "https://%s/rest%s" % (dcnm_hostname, path)

def get_url(url, dcnm_token):
    """ Function to send GET request to DCNM
    """
    url = create_url(path=url)
    print(url)
    headers = {
    'dcnm-token': dcnm_token,
    'content-type': "application/json",
    'Accept': "application/json",
    'cache-control': "no-cache"
    }
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    return response.json()

def put_url(url, dcnm_token, data):
    """ Function to send PUT request to DCNM
    """  
    url = create_url(path=url)
    print(url)
    headers = {
    'dcnm-token': dcnm_token,
    'content-type': "application/json",
    'Accept': "application/json",
    'cache-control': "no-cache"
    }
    try:
        response = requests.put(url, data=json.dumps(data), headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)
    
    return response.json()



def main():
    auth = get_auth_token()
    #print("Dcnm-token is: {}".format(auth['token']))
    
    # Getting all the fabrics
    fabrics = get_url("/control/fabrics", auth['token'])
    fabric_list = []
    for fabric in fabrics:
        fabric_list.append(fabric['fabricName'])

    # List the devices under the specific fabric
    #devices = get_url("/control/fabrics/{fabricName}/inventory".format(fabricName=fabric1_name), auth['token'])
    
    # User prompt to choose fabric
    fabric_list_exit = fabric_list
    fabric_list_exit.insert(0, 'Exit')

    #answer = {'fabric_name':'', 'device_name':''}
    valid_state = True
    valid_state2 = True
    valid_state3 = True
    while valid_state:
        question = [{'type':'list', 'name':"fabric_name", 'message':"Please select the fabric from the list:", 'choices':fabric_list_exit}]
        answer = prompt(question, style=style)
        if answer['fabric_name'] == "Exit":
            print("Exiting...")
            exit(0)
        else:
            devices = get_url("/control/fabrics/{fabricName}/inventory".format(fabricName=answer['fabric_name']), auth['token'])
            # Creating switch:serialNumber dictionary
            switch_and_sn_dict = {}
            switch_and_vpc_dict = {}
            switches = {}
            for device in devices:
                #print(device["logicalName"])
                switch_and_sn_dict.update({device["logicalName"]:device["serialNumber"]})
                switch_param_list = [
                    device["serialNumber"],
                    device["isVpcConfigured"],
                    device["role"],
                    device["peer"]
                ]
                switches.update({device["logicalName"]:switch_param_list})
            # Adding "Go back" to the list
            print(switches)
            switch_and_sn_dict_keys_go_back = list(switch_and_sn_dict.keys())
            switch_and_sn_dict_keys_go_back.insert(0, "Go back")
            # While loop 2 -----------------------------------------------------------------------------------------
            while valid_state2:
                # User prompt to choose switch
                question = [{'type':'list', 'name':"device_name", 'message':"Please select the switch from the list:", 'choices':switch_and_sn_dict_keys_go_back}]
                answer = prompt(question, style=style)
                if answer['device_name'] == "Go back":
                    break
                else:
                    active_device_sn = switch_and_sn_dict[answer['device_name']]
                    active_device_name = answer['device_name']
                    interfaces = get_url("/interface/detail?serialNumber={serialNumber}".format(serialNumber=active_device_sn), auth['token'])
                    question = [
                        {
                            'type':'list',
                            'name':"device_action",
                            'message':"What do you wnat to do with switch:",
                            'choices':[
                                'Get list of all interfaces',
                                'Get list of all connected interfaces',
                                'Get list of all not connected interfaces' 
                            ]
                        }
                    ]
                    answer = prompt(question, style=style)
                    active_interfaces_dict = {}  
                    active_interfaces_list = []     
                    for interface in interfaces:
                        if interface['sysName'] == active_device_name:
                            if "Ethernet" in interface['ifName']:
                                if answer['device_action'] == 'Get list of all interfaces':
                                    active_interfaces_list.append(interface['ifName'])
                                    active_interfaces_dict.update({interface['sysName']:active_interfaces_list})
                                elif answer['device_action'] == 'Get list of all connected interfaces':
                                    if interface['operStatusStr'] == 'up':
                                        active_interfaces_list.append(interface['ifName'])
                                        active_interfaces_dict.update({interface['sysName']:active_interfaces_list})
                                elif answer['device_action'] == 'Get list of all not connected interfaces':
                                    if interface['operStatusStr'] != 'up':
                                        active_interfaces_list.append(interface['ifName'])
                                        active_interfaces_dict.update({interface['sysName']:active_interfaces_list})
                    print(active_interfaces_dict)
                    
                    #valid_state = False
                    #valid_state2 = False
                    
                    # Adding "Go back to interfaces list"
                    active_interfaces_list_go_back = active_interfaces_list
                    active_interfaces_list_go_back.insert(0, 'Go back')
                    #While loop 3 -----------------------------------------------------------------------------------------
                    while valid_state3:
                        question = [{'type':'list', 'name':"interface_name", 'message':"Please select interface from the list:", 'choices':active_interfaces_list_go_back}]
                        answer = prompt(question, style=style)
                        if answer['interface_name'] == "Go back":
                            break
                        else:
                            #print(answer['interface_name'])
                            interface_details = get_url("/interface?serialNumber={serialNumber}&ifName={ifName}".format(serialNumber=active_device_sn, ifName=answer['interface_name']), auth['token'])
                            #print(interface_details)
                            print(json.dumps(interface_details, indent=4))
                            #valid_state = False
                            #valid_state2 = False
                            #valid_state3 = False
                        




if __name__ == "__main__":
    main()