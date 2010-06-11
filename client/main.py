#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#            main.py is part of MetaDoc (Client).
#
# All of MetaDoc is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# MetaDoc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MetaDoc.  If not, see <http://www.gnu.org/licenses/>.
"""main.py - Runs the synchronization procedure

Information sent and recieved depends on handles passed to main.py

Usage:

-h, --help              Displays this help message
-v, --verbose           Verbose mode, outputs loads of stuff
-q, --quiet             Quiet mode, outputs nothing except
                        critical errors
-e                      Send event data
-c                      Send config data
-s                      Send software data
-u                      Fetch user data
-a                      Fetch allocation data
-p                      Fetch project data
-l <log level>          Sets log level
--loglevel=<log level>  

"""
import ConfigParser
import sys
import getopt
import xml.etree.ElementTree

import metahttp 
from metadoc import MetaDoc
from metaelement import MetaElement

from events.definition import Events
from configuration.definition import Configuration
from software.definition import Software

from allocations.definition import Allocations
from users.definition import Users
from projects.definition import Projects

def write_sample_config():
    """
    Creates a default configuration file.
    Used if the config file is missing to create a base to work from.
    """
    f = open("metadoc.conf", "w")
    f.write("# This is a sample configuration file for MetaDoc\n")
    f.write("# It uses Python's ConfigParser, see\n")
    f.write("#\thttp://docs.python.org/library/configparser.html\n")
    f.write("# for details.\n")
    f.write("\n# The standard MetaDoc section\n")
    f.write("[MetaDoc]\n")
    f.write("host  = https://localhost/metadoc_api/\n")
    f.write("key   = userkey.pem\n")
    f.write("cert  = usercert.pem\n")
    f.write("valid = False\n")
    f.close()

def testConfig(vals):
    """
    Tests configuration file to see that it contains the necessary 
    information to run the script.
    """
    if 'valid' in vals:
        if vals['valid'].lower() == "false" or vals['valid'].lower() == "no":
            print "The config is not valid. "
            print "You need to explicitly set the \
                    config-switch 'valid' to 'True'."
            print "You can also remove the switch completely from the file"
            print ""
            print "It is included as a fail-safe to stop \
                    auto-configured programs from running."
            return False
    if 'host' not in vals or vals['host'] == "":
        print "Need a valid host. Aborting"
        return False
    if 'cert' not in vals or vals['cert'] == "":
        print "Need path to the certificate to use for AuthN/AuthZ. Aborting"
        return False
    if 'key' not in vals or vals['key'] == "":
        print "Need path to the privatekey to use for AuthN/AuthZ. Aborting"
        return False
    return True

def main():
    optstr = "hvqecaspul:"
    optlist = ['help', 'dry-run', 'loglevel=']
    # Default settings
    # Will be altered depending on passed options
    verbose = False
    quiet = False
    dryrun = False
    loglevel = 2
    # Information to send
    send_elements = []
    # Fetch information from server
    fetch_elements = []

    try:
        opts, args = getopt.getopt(sys.argv[1:], optstr, optlist)
    except getopt.GetoptError, goe:
        print str(goe)
        print __doc__
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print __doc__
            sys.exit()
        elif opt == '-v':
            verbose = True
        elif opt == '-q':
            quiet = True
        elif opt == '-e':
            send_elements.append(Events)
        elif opt == '-c':
            send_elements.append(Configuration)
        elif opt == '-s':
            send_elements.append(Software)
        elif opt == '-u':
            fetch_elements.append(Users)
        elif opt == '-a':
            fetch_elements.append(Allocations)
        elif opt == '-p':
            fetch_elements.append(Projects)
        elif opt == '--dry-run':
            dryrun = True
        elif opt in ('-l', '--loglevel'):
            loglevel = arg



    conf = ConfigParser.ConfigParser()
    conf.read("metadoc.conf")
    v = []
    vals = {}
    try:
        v = conf.items("MetaDoc")
    except ConfigParser.NoSectionError as nose:
        print "Need a configuration-file. "
        print "A sample file has been created for you in metadoc.conf"
        print "Please edit this file carefully and re-run the program."
        write_sample_config()
        return

    for key,value in v:
        vals[key] = value

    if not testConfig(vals):
        # testConfig() prints any errors
        return

    # ready for main processing.
    m = MetaDoc(True)
    for element in send_elements:
        element_processor = element()
        site_element = element.site_handler()
        site_element.populate()
        element_processor.add_elements(site_element.fetch())
        m.reg_meta_element(element_processor)

    # Get ready to send the data
    if verbose:
        print "-" * 70
        print "Connecting to host: %s" % vals['host']
        print "Using key: %s" % vals['key']
        print "Using certificate: %s" % vals['cert']
        print "-" * 70
    cli = metahttp.XMLClient(vals['host'], vals['key'], vals['cert'])
    res = cli.send(m.get_xml())
    if verbose:
        print "%s\nSent data:\n%s" % ("-" * 70, "-" * 70)
        print m.get_xml()
    if res:
        xml_data = res.read()
        if verbose:
            print "%s\nRecieved data:\n%s" % ("-" * 70, "-" * 70)
            print xml_data
        # FIXME - Error catching
        return_data = xml.etree.ElementTree.fromstring(xml_data)
        element_handlers = []
        for element in fetch_elements:
            found_elements = return_data.findall(element.xml_tag_name)
            sub_elements = []
            for found_element in found_elements:
                sub_elements.append(MetaElement.from_xml_element(found_element, element))
            element_handlers.append(element.update_handler(sub_elements))
        for handler in element_handlers:
            handler.process()
    else:
        # FIXME - No data returned, log event
        pass

if __name__ == "__main__":
    main()

