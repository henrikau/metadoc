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
-l <log level>          Sets log level, availible levels are:
--loglevel=<log level>  debug, info, warning, error, critical
-n, --no-cache          Will not send any cached data

"""
import ConfigParser
import logging
import logging.handlers
import sys
import getopt
import lxml.etree
import urllib2

import metahttp 
from metadoc import MetaDoc
from metaelement import MetaElement
from cacher import Cacher

# Classes that send information to server
from events.definition import Events
from configuration.definition import Configuration
from software.definition import Software

# Classes that retrieve information from server
from allocations.definition import Allocations
from users.definition import Users
from projects.definition import Projects

possible_send_elements = (Events, Configuration, Software,)

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
    f.write("trailing_slash = True\n")
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
    optstr = "hvqecaspunl:"
    optlist = ['help', 'dry-run', 'loglevel=', 'no-cache']
    # Default settings
    # Will be altered depending on passed options
    verbose = False
    quiet = False
    dryrun = False
    send_cache = True
    loglevel = 2
    # Information to send
    send_elements = []
    # Fetch information from server
    fetch_elements = []

    LOG_LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    log_level = logging.NOTSET

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
            log_level = LOG_LEVELS.get(arg.lower(), logging.NOTSET)
        elif opt in ('-l', '--no-cache'):
            send_cache = False

    logging.basicConfig(level=log_level, format=LOG_FORMAT)
    

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
        logging.info("Creating default configuration file.")
        write_sample_config()
        return

    for key,value in v:
        vals[key] = value

    if not testConfig(vals):
        # testConfig() prints any errors
        return

    # ready for main processing.
    for element in send_elements:
        m = MetaDoc(True)
        c = Cacher(element.xml_tag_name)
        cached_data = c.get_cache()
        if cached_data is not None:
            element_processor = element.from_xml_element(cached_data, element)
        else:
            element_processor = element()
        site_element = element.site_handler()
        site_element.populate()
        element_processor.add_elements(site_element.fetch())
        # Let's see if we have some cached data to add
        m.reg_meta_element(element_processor)
        url = "%s%s" % (vals['host'], element.url)
        if vals['trailing_slash'].lower() == 'true' or vals['trailing_slash'].lower() == 'yes':
            url = "%s/" % url
        cli = metahttp.XMLClient(url, vals['key'], vals['cert'])
        if verbose:
            print "-" * 70
            print "Connecting to host: %s" % url
            print "Using key: %s" % vals['key']
            print "Using certificate: %s" % vals['cert']
            print "-" * 70
            print "Sent data:\n%s" % ("-" * 70)
            print m.get_xml()
        try:
            res = cli.send(m.get_xml())
        except (urllib2.HTTPError, urllib2.URLError) as httperror:
            logging.critical("Unable to connect to server address \"%s\", error: %s" % (url, httperror))
            # Since we're unable to send the document to the server, we will 
            # cache it so that we can send it at a later date.
            Cacher(element.xml_tag_name, m)
        else:
            if res:
                # FIXME - Check that the server accepted the data
                xml_data = res.read()
                if verbose:
                    print "%s\nRecieved data:\n%s" % ("-" * 70, "-" * 70)
                    print xml_data
                    print "-" * 70
                m.check_response(xml_data)
            else:
                # FIXME - Error, no data returned.
                pass

    for element in fetch_elements:
        cli = metahttp.XMLClient("%s%s" % (vals['host'], element.url), vals['key'], vals['cert'])
        if verbose:
            print "-" * 70
            print "Connecting to host: %s%s" % (vals['host'], element.url)
            print "Using key: %s" % vals['key']
            print "Using certificate: %s" % vals['cert']
            print "-" * 70
        try:
            res = cli.send()
        except (urllib2.HTTPError, urllib2.URLError) as httperror:
            logging.critical("Unable to connect to server address \"%s%s\", error: %s" % (vals['host'], element.url, httperror))
        else:
            if res:
                xml_data = res.read()
                if verbose:
                    print "%s\nRecieved data:\n%s" % ("-" * 70, "-" * 70)
                    print xml_data
                try:
                    return_data = lxml.etree.fromstring(xml_data)
                except lxml.XMLSyntaxError, e:
                    logging.error("Error parsing XML document from server: ", e)
                else:
                    found_elements = return_data.findall(element.xml_tag_name)
                    sub_elements = []
                    for found_element in found_elements:
                        sub_elements.append(MetaElement.from_xml_element(found_element, element))
                    element.update_handler(sub_elements).process()

if __name__ == "__main__":
    main()

