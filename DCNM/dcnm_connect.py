import http.client
import ssl
import base64
import string
import json
import getpass
import requests
import os

__author__ = "Sergey Dubov"
__copyright__ = "Copyright (c) SD CP"

# Global variable
serverip = "192.168.127.240"

def getRestToken(username, password):
  ssl._create_default_https_context = ssl._create_unverified_context

  ##replace server ip address here
  conn = http.client.HTTPSConnection(serverip)

  payload = "{\"expirationTime\" : 10000000000}\n"

  ## replace user name and password here
  authenStr="%s:%s" % (username, password)

  base64string = base64.encodebytes(bytes(authenStr, 'utf-8'))
  tmpstr= "Basic %s" % base64string
  authorizationStr = tmpstr.replace("b\'","").replace("\\n\'","")
  print(authorizationStr)

  headers = {
      'content-type': "application/json",
      'authorization': authorizationStr,
      'cache-control': "no-cache"
      }

  conn.request("POST", "/rest/logon", payload, headers)

  res = conn.getresponse()
  data = res.read()
  print(data)
  longstr=data.decode("utf-8")
  strArr=longstr.split("\"")
  return strArr[3]

#Function to send GET request to DCNM. Returns GET response only.
def apiget(dcnm_token, api_url):
    headers = {
    'dcnm-token': dcnm_token,
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }
    url = ("https://%s/rest%s" % (serverip, api_url))
    
    requests.packages.urllib3.disable_warnings()            #disable warnings in terminal
    r = requests.get(url, headers=headers, verify=False)    #Change to True, if ssl check is required
    return r

def apiput(dcnm_token, api_url, data):
    headers = {
    'dcnm-token': dcnm_token,
    'Content-Type': "application/json"
    }
    url = ("https://%s/rest%s" % (serverip, api_url))
    
    requests.packages.urllib3.disable_warnings()            #disable warnings in terminal

    r = requests.put(url, data=json.dumps(data), headers=headers, verify=False)
    #r = requests.post(url, json.dumps(data), headers=headers, verify=False)
    return r

def apipost(dcnm_token, api_url, data):
    headers = {
    'dcnm-token': dcnm_token,
    'Content-Type': "application/json"
    }
    url = ("https://%s/rest%s" % (serverip, api_url))
    
    requests.packages.urllib3.disable_warnings()            #disable warnings in terminal

    r = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
    #r = requests.post(url, json.dumps(data), headers=headers, verify=False)
    return r


def getDcnmVer(dcnm_token):
    r = apiget(dcnm_token, "/dcnm-version")   
    data = json.loads(r.text)
    return data['Dcnm-Version']
    #print ("Dcnm version: %s" % data['Dcnm-Version'])

def getDcnmFabric(dcnm_token):
    r = apiget(dcnm_token, "/control/fabrics")
    #print (r.text)
    data = json.loads(r.text)
    #print ("Dcnm Fabric Name is:   %s" % data[0]['fabricName'])
    return data[0]['fabricName']

def getDcnmFabricConfigPreview(dcnm_token, fabric_name):
    r = apiget(dcnm_token, "/control/fabrics/%s/config-preview" % fabric_name)
    #print (r.text)
    data = json.loads(r.text)
    return data
    #print ("Dcnm Fabric Name is:   %s" % data['fabricName'])
    #return data['fabricName']

def getDcnmFabricNetworks(dcnm_token, fabric_name):
    r = apiget(dcnm_token, "/top-down/fabrics/%s/networks" % fabric_name)
    #print (r.text)
    data = json.loads(r.text)
    return data

def getInterfaceConfig(dcnm_token, serialNumber, ifName):
    r = apiget(dcnm_token, "/interface?serialNumber=%s&ifName=%s" % (serialNumber, ifName))
    #print (r.text)
    data = json.loads(r.text)
    return data

def putInterfaceUpdate(dcnm_token, requestbody):
    r = apiput(dcnm_token, "/interface", requestbody)
    data = r
    return data

#new function
def putInterfaceDescUpdate(dcnm_token, serialNumber, ifName, newDesc):
    #get current interface config first
    serialNumber = serialNumber
    ifName = ifName
    interfaceConf = getInterfaceConfig(dcnm_token, serialNumber, ifName)
    interfaceConf[0]['interfaces'][0]['nvPairs']['DESC'] = newDesc
    #update description
    r = apiput(dcnm_token, "/interface", interfaceConf[0])
    data = r
    return data

def postInterfaceDeploy(dcnm_token, serialNumber, ifName):
    requestbody = [{'serialNumber': '', 'ifName': ''}]

    requestbody[0]['serialNumber'] = serialNumber
    requestbody[0]['ifName'] = ifName
    
    requestbody
    r = apipost(dcnm_token, "/interface/deploy", requestbody)
    data = r
    return data

def main():
    #dcnm_ip = "192.168.127.196"
    username = input("Username:")
    password = getpass.getpass("Password:")
    resttoken = getRestToken(username, password)
    print (resttoken)
    
    DcnmVer = getDcnmVer(resttoken)
    print ("Dcnm version is: %s" % DcnmVer)
    
    fabricName = getDcnmFabric(resttoken)
    print ("Dcnm Fabric Name is: %s" % fabricName)

    

    #fabricConfigPreview = getDcnmFabricConfigPreview(resttoken, fabricName)
    #SwitchIDName = {}   #preparing and building dictionary with switchID:switchName
    #for item in fabricConfigPreview:
    #    id = item['switchId']
    #    name = item['switchName']
    #    SwitchIDName[id] = name

    #print (SwitchIDName)
    
       

    ######
    #N9Kv_Leaf_01 = "9FSBOCHR0RY"
    #interfaceName = "Ethernet1/19"
    #interfaceConf = getInterfaceConfig(resttoken, N9Kv_Leaf_01, interfaceName)

    #interfaceConf[0]['interfaces'][0]['nvPairs']['DESC'] = ""
    #print (interfaceConf[0])

    #int = putInterfaceUpdate(resttoken,interfaceConf[0])
    #print (int)

    serialNumber = "9FSBOCHR0RY" #N9Kv-Leaf-01
    ifName = "Ethernet1/20"
    newDesc = "5 June 15:34"

    int = putInterfaceDescUpdate(resttoken, serialNumber, ifName, newDesc)
    if int.status_code == 200:
        print ("Completed successfully - code %s" % int.status_code)
    
    intdeploy = postInterfaceDeploy(resttoken, serialNumber, ifName)
    if intdeploy.status_code == 200:
        print ("Deploy has been completed successfully - code %s" % intdeploy.status_code)



if __name__ == "__main__":
    main()