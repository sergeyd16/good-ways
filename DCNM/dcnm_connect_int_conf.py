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
interfaces_config = 'D:\Python\Workspace1\DCNM\interfaces_config.json'

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
    #print(url)
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
    
    return response



def main():
    auth = get_auth_token()
    #print("Dcnm-token is: {}".format(auth['token']))
    
    with open(interfaces_config) as json_file:
        data = json.load(json_file)
        for interface_config in data:
            #print(interface_config)
            #print(json.dumps(interface_config, indent=4))
            #print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            r = put_url("/interface", auth['token'], interface_config)
            if r.status_code == 200:
                print("Interface {} has been configured successfully on {}.".format(interface_config['interfaces'][0]['ifName'], interface_config['interfaces'][0]['serialNumber']))



if __name__ == "__main__":
    main()