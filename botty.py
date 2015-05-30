#! /usr/bin/env python

'''
    botty.py - A dynamic deployment system for *nix-based OSs.
    Copyright (C) 2014-2015 Foxlet <inquiries@comprepair.tk>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

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
        print(botty.util.getpacks())
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
