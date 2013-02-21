#!/usr/bin/env python
"""Script to gather JSON inventory of running instances"""
import ConfigParser
import json
import os.path
import sys
from novaclient.v1_1 import client

def get_config():
    top_dir  = os.path.abspath(
        os.path.dirname(os.path.abspath(__file__)) + "/..")
    cfg_file = os.path.abspath(top_dir + "/config/config")
    cfg = ConfigParser.ConfigParser()
    if not os.path.exists(cfg_file):
        sys.stderr.write("Could not find configuration\n")
        sys.exit(1)
    cfg.read([cfg_file])
    return cfg

cfg = get_config()
nova = client.Client(
    cfg.get("openstack", "username"),
    cfg.get("openstack", "password"),
    cfg.get("openstack", "tenant_name"),
    cfg.get("openstack", "auth_url"), 
    insecure=True,
)
servers = []
for server in nova.servers.list():
    servers.append({
        created : server.created,
        flavor  : server.flavor,
        id      : server.id,
        image   : server.image.id,
        name    : server.name,
        status  : server.status,
        updated : server.updated,
        user_id : server.user_id,
        metadata: server.metadata,
    })
print json.dumps(servers)
