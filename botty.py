#! /usr/bin/env python

__author__ = 'foxlet'

from fabric.api import env, run, execute, hosts
from botty.help import create_args
import json
import re

VERSION = 1.0
arguments = create_args(VERSION)
servers = arguments.server
print(servers)

if arguments.config:
    with open(str(arguments.config)) as config:
        servers_data = json.load(config)

DataMatch = {}

env.key_filename = '/home/furserv/.ssh/id_rsa'

user = "snoonet"

full_servers = [user + '@'+ server for server in servers]

deploy_to = ['snoonet@con.cosmos.snoonet.org', 'snoonet@con.athena.snoonet.org', 'snoonet@con.veronica.snoonet.org']
pattern = re.compile(r'up (\d+) days')

def uptime():
    res = run('uptime')
    match = pattern.search(res)
    if match:
        days = int(match.group(1))
        DataMatch['uts'].append(days)

def find_arch_snoo():
    res = run('file /bin/ls')

def get_sign_binary():
    res = run('openssl sha1 /home/snoonet/inspircd/bin/inspircd')
    if res != 'SHA1(/home/snoonet/inspircd/bin/inspircd)= 6cd808d4fd6ab7330c50132f31d97a7d11b44356':
        print('Ready for Upgrade')

def execute_upgrade():
    res = run('openssl sha1 /home/snoonet/inspircd/bin/inspircd')
    if res != 'SHA1(/home/snoonet/inspircd/bin/inspircd)= 6cd808d4fd6ab7330c50132f31d97a7d11b44356':
        print('Ready for Upgrade')
        res2 = run('cd /home/snoonet/inspircd/ && wget http://eu.furcode.co/buildbot/snoonet/inspircd.2.0.20.buildbot.tar.gz && killall inspircd && tar -xvf inspircd.2.0.20.buildbot.tar.gz && ./inspircd start')
    else:
        print('Ignoring, already on latest.')

def main():
    DataMatch['uts'] = []

    execute(find_arch_snoo, hosts=full_servers)


if __name__ == '__main__':
    main()