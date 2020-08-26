from cvplibrary import Form
from jsonrpclib import Server
from cvplibrary import CVPGlobalVariables, GlobalVariableNames

#fetching the management ip of the current device
device_ip = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_IP)
#fetching the username for the current device
username = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_USERNAME)
#fetching the password for the current device
password = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_PASSWORD)

#fetching the variables from the form
intvlan_var =  Form.getFieldById("field_1").getValue();
vrf_var = Form.getFieldById("field_2").getValue();
ipaddrv = Form.getFieldById("field_3").getValue();

print "vrf definition " + vrf_var

print "vlan "+ intvlan_var
print "interface vlan "+ intvlan_var
print "mtu 9000"
print "no autostate"
print "vrf forwarding " + vrf_var
print "ip address virtual " + ipaddrv + "/24"

print "interface Vxlan1"
print "vxlan vlan " + intvlan_var + " vni " +  intvlan_var

#connecting to the switch
switch = Server('https://%s:%s@%s/command-api' % (username, password, device_ip))
#fetching the bgp local as number
response = switch.runCmds( 1, ["show ip bgp"] , "json")
bgpasn = response[0]["vrfs"]["default"]["asn"]
#fetching the current vlan bundle under the selected VRF
response = switch.runCmds( 1, [
"show running-config"] , "json")
cur_vlan_bundle_kv = (response[0]["cmds"]["router bgp %s" %bgpasn]["cmds"]["vlan-aware-bundle Mac-Vrf-%s" %vrf_var]["cmds"])

cur_vlan_bundle_kv = str(cur_vlan_bundle_kv)
cur_vlan_bundle_kv = cur_vlan_bundle_kv.split("vlan",1)[1].split("'",1)[0]
new_vlan_bundle = cur_vlan_bundle_kv + "," + intvlan_var

print "router bgp "+ str(bgpasn)
print "vlan-aware-bundle Mac-Vrf-" + vrf_var
print "vlan "+ new_vlan_bundle

