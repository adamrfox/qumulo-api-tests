#!/usr/bin/python
from __future__ import print_function

import sys
import getopt
import getpass
import requests
import base64
import json
import urllib3
urllib3.disable_warnings()

def usage():
    print("Usage Goes Here!")
    exit(0)

def dprint(message):
    if DEBUG:
        print(message + "\n")

def python_input (message):
    if int(sys.version[0]) > 2:
        value = input(message)
    else:
        value = raw_input(message)
    return(value)

if __name__ == "__main__":
    DEBUG = False
    token = ""
    user = ""
    password = ""
    headers = {}
    timeout = 360

    optlist, args = getopt.getopt(sys.argv[1:], 'hDt:c:', ['--help', '--DEBUG', '--token=', '--creds='])
    for opt, a in optlist:
        if opt in ['-h', '--help']:
            usage()
        if opt in ['-D', '--DEBUG']:
            DEBUG = True
        if opt in ['-t', '--token']:
            token = a
        if opt in ['-c', '--creds']:
            (user, password) = a.split(':')
        qumulo = args[0]
        headers = {'Content-Type': 'application/json'}
        if not token:
            if not user:
                user = python_input("User: ")
            if not password:
                password = getpass.getpass("Password: ")
            payload = {'username': user, 'password': password}
            payload = json.dumps(payload)
            autht = requests.post('https://' + qumulo + '/api/v1/session/login', headers=headers, data=payload, verify=False, timeout=timeout)
            dprint(str(autht.ok))
            auth = json.loads(autht.content.decode('utf-8'))
            dprint(str(auth))
            if autht.ok:
                auth_headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + auth['bearer_token']}
            else:
                sys.stderr.write("ERROR: " + auth['description'] + '\n')
                exit(2)
        else:
            auth_headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + token}
        dprint("TOKEN:" + str(auth_headers))
        net_data = requests.get('https://' + qumulo + '/v2/network/interfaces/1/status/', headers=auth_headers,verify=False, timeout=timeout)
        dprint(net_data.content)
        net_info = json.loads(net_data.content.decode('utf-8'))
        for node in net_info:
            if node['interface_details']['cable_status'] == "CONNECTED" and node['interface_details']['interface_status'] == "UP":
                for ints in node['network_statuses']:
                    static = ints['address']
                    floats = ints['floating_addresses']
                print(node['node_name'] + " : " + static + "  " + str(floats))




