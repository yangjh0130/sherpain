import os
import time

i = 0

bash_command ="./nnm --config \"Monitored Network IP Addresses and Ranges\"" 

for i in range(0,192):
    bash_command = bash_command + " 192.168."+ str(i) + ".0/24,"
    
    os.system(bash_command)
    time.sleep(7200)
