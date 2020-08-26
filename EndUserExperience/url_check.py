import requests
import sys
import os


__author__ = "Sergey Dubov"
__copyright__ = "Copyright (c) SD CP"



# Global variable


def main():
    try:
        print ("Name of the script: %s \n URL: %s \n WARN: %s \n CRIT: %s" % (sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3]))
    except IndexError:
        print ("No agruments provided")
        sys.exit(2)
    
    #cmd = "\"D:\cURL\bin\curl -X POST -d @\"D:\cURL\bin\format.txt\" https://ynet.co.il -o NUL -s -w \"\nLookup time:\t%{time_namelookup}\nConnect time:\t%{time_connect}#\nPreXfer time:\t%{time_pretransfer}\nStartXfer time:\t%{time_starttransfer}\n\nTotal time:\t%{time_total}\n\""
    #p = os.popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=False)
        


if __name__ == "__main__":
    main()

