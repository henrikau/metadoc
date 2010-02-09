#!/usr/bin/env python
"""
XML Server main startup file.

usage: python main.py

Note: you will have to add server-variables to he config.
"""
import sys, re, getopt
from Config import Config
from HTTPS_Server import HTTPS_Server

def comp_arg(target, argument):
    """
    compare a target argument (target) with a supplied argument (argument)

    params:
    target:     the argument we're looking for
    argument:   the supplied argument.

    The function will strip any enclosing spaces as well as -'s
    """
    if not target or not argument:
        return False

    match = re.compile('[a-z]+', re.IGNORECASE).match(argument)
    if not match:
        return False
    return match.group() == target

def show_help():
    """
    Show usage-information
    """
    print "Usage: %s" % (sys.argv[0])
    print "\t-b\t--bootstrap\tBootstrap the system"
    print "\t-h\t--help\t\tShow this help"
    print "\t-k\t--key\t<key>\tAdd path to server-key to config"
    print "\t-c\t--cert\t<cert>\tAdd path to server-key (X.509, pam-encoded) to config"
    print "No argument will start the server"

def bootstrap(config):
    """
    Bootstrap system, make it ready to use.

    Note: this will remove the path to the key and certificate. If this
    is set, it must be re-added!
    """
    if not config:
        print "No config provided"
        return
    config.set('server_address', 'localhost')
    config.set('server_port', '8443')
    config.set('server_cert_path', '/dev/zero/')
    config.set('server_key_path', '/dev/zero/')

def dump(config):
    """
    Dump config-vars to stdout
    """
    if not config:
        return
    res = config.getAll()
    for line in res:
        if len(line) == 2:
            print "%s\t%s" % (line[0], line[1])

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hbckd",
                                   ["help", "boostrap", "cert", "key", "dump"])
    except getopt.GetoptError as ge:
        print ge
        sys.exit(255)

    config = Config('XML_Server_config.sql')
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            show_help()
        elif opt in ('-b', '--bootstrap'):
            bootstrap(config)
        elif opt in ('-k', '--key'):
            if args[0]:
                config.set('server_key_path', args[0])
                print "Path to server-key successfully updated"
        elif opt in ('-c', '--cert'):
            if args[0]:
                config.set('server_cert_path', args[0])
                print "Path to server-certificate successfully updated"
        elif opt in ('-d', '--dump'):
            dump(config)
        sys.exit(0)

    if config.first_run():
        print "First time we run server, bootstrapping database"
        print "You should set the path to SSL-key and -certificate"
        bootstrap(config)

    server = HTTPS_Server(config)
    server.start()

