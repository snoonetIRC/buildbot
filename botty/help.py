__author__ = 'foxlet'

import argparse

def create_args(VERSION):
    options = argparse.ArgumentParser(description='BuildBot for Linux {}'.format(str(VERSION)))
    options.add_argument('server', metavar='server(s)', nargs='*')
    options.add_argument('-p', '--package', help='compile a different package rather than the default in servers.json')
    options.add_argument('-c', '--config', help ='use a custom configuration instead of servers.json')
    options.add_argument('-l', '--list', help='list the current servers in the rotary and their archs', action='store_true')
    options.add_argument('-s', '--ssh', help='assume the server is an user@hostname:port set', action="store_true")
    arguments = options.parse_args()
    return arguments