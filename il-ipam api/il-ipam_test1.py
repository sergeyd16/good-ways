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
ipam_hostname = "il-ipam.checkpoint.com"
token = "fomHdiokuimgHkITXxWfIrhK4q0DAmaX"

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

def get_auth_token(ipam_hostname=ipam_hostname):
    """ Authenticates with controller and returns a token to be used in subsequent API invocations
    """
    username = input("Username:")
    password = getpass.getpass("Password:")
    
    # Print login message to terminal
    print("----------------------------------------------------")
    print("Login to {} as {} ...".format(ipam_hostname, username))

    login_url = "https://{}/api/ilipam/user/".format(ipam_hostname)
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
    
    global token
    token = result.json()["data"]["token"]
    
    print("----------------------------------------------------")
    print("You have successfully logged in as {}.".format(username))
    print("----------------------------------------------------")
    
    return {
        "ipam_hostname": ipam_hostname,
        "token": token
    }

def create_url(path, ipam_hostname=ipam_hostname):
    """ Helper function to create a il-ipam (PHPIPAM) API endpoint URL
    """
    return "https://%s/api/ilipam%s" % (ipam_hostname, path)

def get_url(url):
    """ Function to send GET request to il-ipam
    """
    url = create_url(path=url)
    print(url)
    headers = {
    'token': token,
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

def search_for_subnet (CIDR):
    response = get_url("/subnets/search/{}/".format(CIDR))
    return response

def search_first_free_ip (subnet_id):
    response = get_url("/subnets/{}/first_free/".format(subnet_id))
    return response




def main():
    #auth = get_auth_token()    
    #print("il-ipam-token is: {}".format(auth['token']))
    #github test
    print("Static il-ipam-token is: {}".format(token))

    subnet = search_for_subnet("192.168.187.0/24")
    subnet_id = subnet['data'][0]['id']

    free_ip = search_first_free_ip(subnet_id)
    print(free_ip['data'])

    




if __name__ == "__main__":
    main()