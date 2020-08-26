#!/usr/bin/python
import requests, json, sys
request_url = "https://gr-icinga-master.checkpoint.com:5665/v1/objects/services"

headers = {
        'Accept': 'application/json',
        'X-HTTP-Method-Override': 'GET'
        }

data = {
        "attrs": [ "name", "state" ],
        "joins": [ "host.name" ],
        "filter": "service.name == name && service.state == state && service.state_type == 1" ,
        "filter_vars": { "name": "te.emu.restarts", "state": 2 }
}

def main():
    us_list = []
    gr_list = []
    r = requests.post(request_url,
            headers=headers,
            auth=('root', 'icinga'),
            data=json.dumps(data),
            verify="/var/lib/icinga2/certs/ca.crt")
    if (r.status_code == 200):
        exit_code = 0
    else:
            print r.text
            r.raise_for_status()
    all_emulators = r.json()
    for item in all_emulators['results']:
        if str(item['joins']['host']['name']).startswith('us'):
            us_list.append(item)
        elif str(item['joins']['host']['name']).startswith('gr'):
            gr_list.append(item)
    if len(us_list) != 0:
        print "Following emulators in US was restarted in last 24 hours:"
        for item in us_list:
            print item['joins']['host']['name']
        if len(us_list) >= 10:
            exit_code = 2
    if len(gr_list) != 0:
        print "\nFollowing emulators in GR was restarted in last 24 hours:"
        for item in gr_list:
            print item['joins']['host']['name']
        if len(us_list) >= 10:
            exit_code = 2
    print '|us_site_restarts='+str(len(us_list))+';;10 gr_site_restarts='+str(len(gr_list))+';;10'
 


    sys.exit(exit_code)

if __name__ == '__main__':
    main()