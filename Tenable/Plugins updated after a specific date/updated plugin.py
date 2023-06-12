from tenable.sc import TenableSC
import csv
import getpass
import time
from datetime import datetime


sc_ip = input("TSC IP: ")
sc_port = int(input("TSC_Port: "))
sc_id = input("TSC ID: ")
sc_pw = getpass.getpass("TSC PW: ")
select_date = input("날짜 입력 (YYYY-MM-DD 형식으로 입력): ")

input_time = "%s 00:00:00" % (select_date)
unix_timestamp = str(time.mktime(time.strptime(input_time, "%Y-%m-%d %H:%M:%S")))
print(unix_timestamp)

sc = TenableSC(sc_ip, port=sc_port)
sc.login(sc_id, sc_pw)

plugins = sc.plugins.list(fields=['id', 'name', 'family', 'pluginModDate'], filter=('pluginModDate', 'gte', unix_timestamp))

with open("updated_plugins.csv", 'w', newline='') as f:
    writer = csv.writer(f)

    headers = ['ID', 'Name', 'Family', 'Update Date']
    writer.writerow(headers)

    for plugin in plugins:
        plugin_id = plugin['id']
        plugin_name = plugin['name'].replace(",", " ")
        plugin_family = plugin['family']['name']
        plugin_dt = datetime.fromtimestamp(int(plugin['pluginModDate']))
        plugin_date = plugin_dt.date()
        writer.writerow([plugin_id, plugin_name, plugin_family, plugin_date])
        print(f"{plugin_id}, {plugin_name}, {plugin_family}, {plugin_date}")
