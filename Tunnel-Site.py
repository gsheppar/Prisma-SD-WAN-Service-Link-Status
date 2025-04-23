#!/usr/bin/env python3
import prisma_sase
import argparse
from prisma_sase import jd, jd_detailed
import sys
import logging
import os
import datetime
import collections
import csv 



# Global Vars
SCRIPT_NAME = 'SDWAN: VPN Tunnel Down'
SCRIPT_VERSION = "v1"

# Set NON-SYSLOG logging to use function name
logger = logging.getLogger(__name__)

##############################################################################
# Prisma SD-WAN Auth Token
##############################################################################

sys.path.append(os.getcwd())
try:
    from prismasase_settings import PRISMASASE_CLIENT_ID, PRISMASASE_CLIENT_SECRET, PRISMASASE_TSG_ID

except ImportError:
    PRISMASASE_CLIENT_ID=None
    PRISMASASE_CLIENT_SECRET=None
    PRISMASASE_TSG_ID=None

def tunnels(sase_session, site_name, endpoint_ip, status):
         
    for site in sase_session.get.sites().cgx_content["items"]:
        if site["name"] == site_name:
            print("Checking site " + site["name"])
            for element in sase_session.get.elements().cgx_content["items"]:
                if element['site_id'] == site["id"]:
                    for interface in sase_session.get.interfaces(site_id=site["id"], element_id=element["id"]).cgx_content["items"]:
                        if interface["type"] == "service_link":
                            try:
                                if interface["service_link_config"]["peer"]["ip_addresses"][0] == endpoint_ip:
                                    if str(interface["admin_up"]) == status:
                                        print("Interface " + interface["name"] + " is already admin up " + str(status))
                                    else:
                                        interface["admin_up"] = status
                                        resp = sase_session.put.interfaces(site_id=site["id"], element_id=element["id"], interface_id=interface["id"],data=interface)
                                        if not resp:
                                            print(str(jdout(resp)))
                                            print("Error changing interface " + interface["name"])
                                        else:
                                            print("Interface " + interface["name"] + " changed to admin up " + str(status))
                            except:
                                print("Failed checking interface " + interface["name"])
            
    return

                                          
def go():
    ############################################################################
    # Begin Script, parse arguments.
    ############################################################################
    
    parser = argparse.ArgumentParser()
             
    # Allow Controller modification and debug level sets.
    config_group = parser.add_argument_group('Config', 'These options change how the configuration is generated.')
    config_group.add_argument('--site', '-S', help='Site name', required=True)
    config_group.add_argument('--ip', '-I', help='IP', required=True)
    config_group.add_argument('--enabled', '-E', help='Enabled or not (true/false)', required=True)

    
    sase_session = prisma_sase.API()
    sase_session.set_debug(0)
    args = vars(parser.parse_args())
    
    site_name = args['site']
    endpoint_ip = args['ip']
    status = args['enabled']
    if status != "False" and status != "True":
        print("Status must be either True or False")
        return

    sase_session.interactive.login_secret(client_id=PRISMASASE_CLIENT_ID,
                                          client_secret=PRISMASASE_CLIENT_SECRET,
                                          tsg_id=PRISMASASE_TSG_ID)
    if sase_session.tenant_id is None:
        print("ERR: Login Failure. Please provide a valid Service Account")
        sys.exit()    

    tunnels(sase_session, site_name, endpoint_ip, status)
    
    # end of script, run logout to clear session.
    
if __name__ == "__main__":
    go()