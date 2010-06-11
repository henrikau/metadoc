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

from events import Events
from custom.siteevents import SiteEvent
from configuration import Configuration
from custom.siteconfiguration import SiteConfiguration
from software import Software
from custom.sitesoftware import SiteSoftware

from allocations import Allocations
from users import Users
from projects import Projects

fetch_elements = (Allocations,Users,Projects,)


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
    optstr = "hvqecsual:"
    optlist = ['help', 'dry-run', 'loglevel=']
    # Default settings
    # Will be altered depending on passed options
    verbose = False
    quiet = False
    dryrun = False
    loglevel = 2
    # Information to send
    events = False
    configuration = False
    software = False
    # Fetch information from server
    user = False
    allocation = False

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
            events = True
        elif opt == '-c':
            configuration = True
        elif opt == '-s':
            software = True
        elif opt == '-u':
            user = True
        elif opt == '-a':
            allocation = True
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
    if configuration:
        xml_configuration = Configuration()
        siteconfig = SiteConfiguration()
        siteconfig.populate()
        config_entries = siteconfig.fetch()
        for config_entry in config_entries:
            xml_configuration.add_element(config_entry)
        m.reg_meta_element(xml_configuration)
    if events:
        xml_event = Events()
        site_events = SiteEvent()
        site_events.populate()
        event_entries = site_events.fetch()
        for event_entry in event_entries:
            xml_event.add_element(event_entry)
        m.reg_meta_element(xml_event)
    if software:
        xml_software = Software()
        site_software = SiteSoftware()
        site_software.populate()
        software_entries = site_software.fetch()
        for software_entry in software_entries:
            xml_software.add_element(software_entry)
        m.reg_meta_element(xml_software)

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
        elmnts = []
        for element in fetch_elements:
            found_elements = return_data.findall(element.xml_tag_name)
            for found_element in found_elements:
                elmnts.append(MetaElement.from_xml_element(found_element, element))
        for ele in elmnts:
            print ele.xml_tag_name, ele.attributes
            for ell in ele.sub_elements:
                print ell.xml_tag_name, ell.attributes
    else:
        # FIXME - No data returned, log event
        pass

if __name__ == "__main__":
    main()

