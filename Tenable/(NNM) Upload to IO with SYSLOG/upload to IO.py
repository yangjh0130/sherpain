import re
from tenable.io import TenableIO

io_ACCESS_KEY = "5b098f94c4a4b5c28b7e2639e4747bc8bb495d18bc3975285079ed211c138e64"
io_SECRET_KEY = "8a747b30a2ed2eefcfcc78d5252252a2acd5e1bb913a20f18efb527e6df57de4"

tio = TenableIO(io_ACCESS_KEY, io_SECRET_KEY)

filepath = './syslog.log'

mac_pattern = "([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"
ip_pattern = "nnm: (25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}"

with open(filepath) as fp:
    line = fp.readline()

    while line:
        ip_str = re.search(ip_pattern, line)
        ip_add = (ip_str.group()[5:])

        mac_str = re.search(mac_pattern, line)
        mac_add = (mac_str.group())

        print(ip_add, mac_add)

        rs = tio.assets.asset_import('example_source', {
            'ipv4': [ip_add],
            'mac_address': [mac_add],
            })
        print(tio.assets.import_job_details(rs))
        print(fp.tell())
        line = fp.readline()
