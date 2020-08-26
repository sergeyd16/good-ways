import requests
import sys
import os


__author__ = "Sergey Dubov"
__copyright__ = "Copyright (c) SD CP"



# Global variable
#Lookup time:       curl[1]
#Connect time:      curl[2]
#PreXfer time:      curl[3]
#StartXfer time:    curl[4]

#Total time:        curl[5]



def main():
    try:
        #print ("Name of the script test Sergey: %s|load_time=%s;%s;%s" % (sys.argv[0], sys.argv[2], sys.argv[2], sys.argv[3]))
        #mycurl_time = []
        warning_threshold = sys.argv[2]
        critical_threshold = sys.argv[3]
        
        warning_threshold_dns = 2
        critical_threshold_dns = 5

        mycurl_time_proxy = []
        proxy_address = "http://" + sys.argv[4] + ".checkpoint.com:8080"
        #mycurl_string = "\"C:\Program Files\ICINGA2\icinga_scripts\curl_tool\curl.exe\" " + sys.argv[1] + " -o NUL -s -w \"%{time_namelookup},%{time_connect},%{time_pretransfer},%{time_starttransfer},%{time_total}\""
        
        if sys.argv[4] == "noproxy":
            mycurl_string_proxy = "\"C:\Program Files\ICINGA2\icinga_scripts\curl_tool\curl.exe\" " + sys.argv[1] + " -o NUL -s -w \"%{time_namelookup},%{time_connect},%{time_pretransfer},%{time_starttransfer},%{time_total}\""
        else:    
            mycurl_string_proxy = "\"C:\Program Files\ICINGA2\icinga_scripts\curl_tool\curl.exe\" " + sys.argv[1] + " -o NUL -x " + proxy_address + " -s -w \"%{time_namelookup},%{time_connect},%{time_pretransfer},%{time_starttransfer},%{time_total}\""
        
        #print (mycurl_string_proxy)

        #cmd = os.popen("\"C:\Program Files\ICINGA2\icinga_scripts\curl_tool\curl.exe\" https://ynet.co.il -o NUL -s -w \"%{time_namelookup},%{time_connect},%{time_pretransfer},%{time_starttransfer},%{time_total}\"").read()
        
        # Below line must be uncommmented, if we want to test without proxy as well
        #cmd = os.popen(mycurl_string).read()
        
        cmd_proxy = os.popen(mycurl_string_proxy).read()
        #mycurl_time = cmd.split(",")
        mycurl_time_proxy = cmd_proxy.split(",")

# Checking curl time status
        if mycurl_time_proxy[4] < warning_threshold:
            test_status = "OK" 
            my_exit_code = 0       
        elif warning_threshold < mycurl_time_proxy[4] < critical_threshold:
            test_status = "WARNING"
            my_exit_code = 1
        else:
            test_status = "CRITICAL"
            my_exit_code = 2

# Checking dns time status
        if mycurl_time_proxy[0] < warning_threshold:
            test_status_dns = "OK"       
        elif warning_threshold < mycurl_time_proxy[0] < critical_threshold:
            test_status_dns = "WARNING"
        else:
            test_status_dns = "CRITICAL"     
        



        #print ("curl time to %s is %s|curl_load_time=%s;%s;%s" % (sys.argv[1], mycurl_time[4], mycurl_time[4], sys.argv[2], sys.argv[3]))
        print ("%s - curl time to %s is %s|curl_load_time=%s;%s;%s" % (test_status, sys.argv[1], mycurl_time_proxy[4], mycurl_time_proxy[4], sys.argv[2], sys.argv[3]))
        print ("%s - dns resolve time to %s is %s|dns_resolve_time=%s;%s;%s" % (test_status_dns, sys.argv[1], mycurl_time_proxy[0], mycurl_time_proxy[0],warning_threshold_dns,critical_threshold_dns))
      
        #print ("proxy dns resolve time to %s is %s|proxy_dns_resolve_time=%s;%s;%s" % (sys.argv[1], mycurl_time_proxy[0], mycurl_time_proxy[0], sys.argv[2], sys.argv[3]))

        sys.exit(my_exit_code)
    except IndexError:
        print ("No agruments provided")
        sys.exit(2)
    
    
    #cmd = "\"D:\cURL\bin\curl -X POST -d @\"D:\cURL\bin\format.txt\" https://ynet.co.il -o NUL -s -w \"\nLookup time:\t%{time_namelookup}\nConnect time:\t%{time_connect}#\nPreXfer time:\t%{time_pretransfer}\nStartXfer time:\t%{time_starttransfer}\n\nTotal time:\t%{time_total}\n\""
    #p = os.popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=False)
        


if __name__ == "__main__":
    main()