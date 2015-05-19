#! /usr/bin/env python

__author__ = 'foxlet'

from fabric.api import env, run, execute, hosts
from fabric import network
from botty.help import create_args
import botty.util
import json
import sys
import tabulate

VERSION = 1.1
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
    elif arguments.ssh:
        servers = list(arguments.server)
else:
    for item in servers_data['servers']:
        servers.append(item['user'] + '@'+ item['host'])

if not servers:
    print('Entering interactive mode.')

for item in servers_data['keys']:
    keys.append(item['path'])

env.key_filename = keys

def main():
    print('Buildbot for Linux {} - built by Foxlet'.format(VERSION))
    print('-'*56 +'\n')
    if arguments.uptime:
        output = {'uts':[]}
        execute(botty.util.uptime, hosts=servers, times=output)
        print('--- Average Server Uptime ' + '-'*30)
        print('    {} days'.format(sum(output['uts'])/len(output['uts'])))
        print('-'*56)
    elif arguments.arch:
        output = []
        execute(botty.util.find_arch, hosts=servers, list=output)
        for x in range(0, len(output)):
            print('{} is {} bits'.format(servers[x], output[x]))
    else:
        print(tabulate.tabulate([[x] for x in servers], ['Servers selected'], tablefmt="psql"))
        print('\nAssuming deployment with specified server(s) and package.')
        if botty.util.getcheck(raw_input('Continue with deployment? [y/N] ').lower()) == False:
            sys.exit(0)
        print('Starting deployment.')
        with open('packages/inspircd-binary.json') as snippet:
            data = json.load(snippet)
        execute(botty.util.deploy_builtin, hosts=servers, snippet=data)
    network.disconnect_all()
if __name__ == '__main__':
    main()