#! /usr/bin/env python

__author__ = 'foxlet'

from fabric.api import env, run, execute, hosts
from botty.help import create_args
import botty.util
import json
import sys

VERSION = 1.0
arguments = create_args(VERSION)
servers = []
keys = []

if arguments.config:
    try:
        with open(str(arguments.config)) as config:
            servers_data = json.load(config)
    except IOError:
        print('Config file {} not found.'.format(arguments.config))
        sys.exit(1)
else:
    try:
        with open('servers.json') as config:
            servers_data = json.load(config)
    except IOError:
        print('Config file servers.json not found.')
        sys.exit(1)

if arguments.server:
    if not arguments.ssh:
        for item in servers_data['servers']:
            if item['name'] in arguments.server:
               servers.append(item['user'] + '@'+ item['host'])
else:
    for item in servers_data['servers']:
        servers.append(item['user'] + '@'+ item['host'])

if not servers:
    print('Entering interactive mode.')

for item in servers_data['keys']:
    keys.append(item['path'])

env.key_filename = keys


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
    if arguments.uptime:
        output = {'uts':[]}
        execute(botty.util.uptime, hosts=servers, times=output)
        print('--- Average Server Uptime ' + '-'*30)
        print('    {} days'.format(sum(output['uts'])/len(output['uts'])))
        print('-'*56)
    else:
        output = []
        execute(botty.util.find_arch, hosts=servers, list=output)
        print(output)

if __name__ == '__main__':
    main()