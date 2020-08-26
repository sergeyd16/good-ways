#!/usr/bin/python
import commands,json,sys,re,socket

def get_lock(process_name):
    get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        get_lock._lock_socket.bind('\0' + process_name)
    except socket.error:
        print ('Script already running')
        sys.exit()

def get_speed(host):
    result_speed = {}
    result_speed['route'] = host['name']
    ipref_command = 'iperf -c '+str(host['address'])+' -f K -r -p '+str(host['port'])+' -t 3 -w 64K'
    output = commands.getoutput(ipref_command)
    raw_speed = re.findall('(KBytes)\s*(\d*)\s*(KBytes\/sec)',str(output))
    try:
        result_speed['inbound'] = raw_speed[0][1]
    except IndexError:
        result_speed['inbound'] = 'null'
    try:
        result_speed['outbound'] = raw_speed[1][1]
    except IndexError:
        result_speed['outbound'] = 'null'
    return result_speed

def human_print_recursive(data):
    if type(data) == dict:
            for key,value in data.items():
                    print (key+':'),
                    human_print(value)
    elif type(data) == list:
            for item in data:
                human_print(item)
    else:
            print (data)

def human_print_table(data):
    print ('<table>')
    print ('<tr><th>Route</th><th>Inbound</th><th>Outbound</th><tr>')
    for item in data:
        print ('<tr>')
        print ('<td>'+item['route']+'</td>'+'<td>'+item['inbound']+'</td>'+'<td>'+item['outbound']+'</td>')
        print ('</tr>')
    print ('</table>')

def human_print(data):
    for item in data:
        print (item['route']+':')
        print ('Inbound: ',item['inbound'])
        print ('Outbound: ',item['outbound'])
        print ('\n')
    
def perfdata_print(data):
    print ('|'),
    for item in data:
        if item['inbound'].isdigit() and item['outbound'].isdigit():
            print (item['route']+'-inbound='+item['inbound']+';;'),
            print (item['route']+'-outbound='+item['outbound']+';;'),

def main():
    hosts_file = '/usr/lib64/nagios/plugins/iperf/hosts.json'
    get_lock('iperf_check.py')
    test_results = []
    with open(hosts_file) as hosts_file:
            hosts_list = json.load(hosts_file)

    for host in hosts_list:
        test_results.append(get_speed(host))

    human_print(test_results)
    perfdata_print(test_results)

if __name__ == "__main__":
    main()