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

Information sent and recieved depends on handles passed to main.py.
If main.py is run without any handles it will attempt to send any cached 
information to the server.

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
--dry-run               Does a dry run, not sending or fetching any data.
                        Run with verbose to see input and output that would be
                        sent.

"""
import ConfigParser
import logging
import logging.handlers
import sys
import os
import getopt
import lxml.etree
import urllib2
import StringIO
import datetime

import metahttp 
import metadoc
import utils
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

# This list is used to check for cached items for elements within the list.
possible_send_elements = [Events, Configuration, Software,]

def write_sample_config():
    """Creates a default configuration file.
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
    f.write("site_name = SITENAME\n")
    f.close()

def testConfig(vals):
    """Tests configuration file to see that it contains the necessary 
    information to run the script.

    """
    if 'valid' in vals:
        if vals['valid'].lower() == "false" or vals['valid'].lower() == "no":
            print "The config is not valid. "
            print ("You need to explicitly set the "
                    "config-switch 'valid' to 'True'.")
            print "You can also remove the switch completely from the file"
            print ""
            print ("It is included as a fail-safe to stop "
                    "auto-configured programs from running.")
            logging.critical("Configuration file not set to valid. "
                    "Please make sure configuration file is correct and "
                    "set 'valid' to 'True'.")
            return False
    if 'host' not in vals or vals['host'] == "":
        print "Need a valid host. Aborting"
        logging.critical("Configuration file missing 'host'.")
        return False
    if 'cert' not in vals or vals['cert'] == "":
        print "Need path to the certificate to use for AuthN/AuthZ. Aborting"
        logging.critical("Configuration file missing path to certificate.")
        return False
    if 'key' not in vals or vals['key'] == "":
        print "Need path to the privatekey to use for AuthN/AuthZ. Aborting"
        logging.critical("Configuration file missing path to private key.")
        return False
    if 'site_name' not in vals or vals['site_name'] == "":
        print "Missing site name in configuration file. Aborting"
        logging.critical("Configuration file missing site name.")
        return False
    return True

def get_element_processor(element, send_cache, verbose, dryrun):
    """Gets an instance of `element` that contains cached data, depending on 
    arguments passed.

    Will skip any cached data if `send_cache` is False or `dryrun` is True.

    """
    if dryrun or not send_cache:
        return element()
    if send_cache:
        c = Cacher(element.xml_tag_name)
        cached_data = c.get_cache()
        if cached_data is not None:
            if element.resend_cache:
                element_processor = element.from_xml_element(cached_data, element)
            else:
                logging.info(("Found cached data for \"%s\", but element "
                    "type declares not to resend this cache. "
                    "Cache removed.") % element.xml_tag_name)
                c.remove_cache()
                element_processor = element()
            if element_processor is None:
                logging.error(("Found cached data for \"%s\", but unable to "
                    "load. Check file \"%s\" for possible errors.") % 
                                (element.xml_tag_name, c.file_path))
                element_processor = element()
            else:
                # We have successfully loaded the cached data.
                if element.resend_cache:
                    logging.debug(("Succesfully loaded cache for \"%s\", "
                        "removing cached file \"%s\".") % 
                        (element.xml_tag_name, c.file_path))
                    c.remove_cache()
        else:
            logging.debug(("Found no cached data for \"%s\".") % 
                            element.xml_tag_name)
            element_processor = element()
    return element_processor

def send_element(element, conf, send_cache, dryrun, verbose, cache_only):
    """Attempts to gather and send information defined by `element` to server.

    If `send_cache` or `dryrun` is False, cache will be ignored.
    If `cache_only` is True, only cache is checked and no new data is gathered.

    """
    if dryrun and cache_only:
        # We're doing a dry run and we've reached the cached items
        return
    m = MetaDoc(conf.get("site_name"))
    element_processor = get_element_processor(element, send_cache, 
                                                verbose, dryrun)
    if not cache_only:
        # If we're doing cache only, we've reached the possible_send_elements
        # loop and do not want or need to remove elements from it anymore.
        possible_send_elements.remove(element)
        site_element = element.site_handler()
        site_element.populate()
        element_processor.add_elements(site_element.fetch())
    m.reg_meta_element(element_processor)
    # Build URL
    url = "%s%s" % (conf['host'], element.url)
    if conf.get('trailing_slash',"").lower() == 'true'\
        or conf.get('trailing_slash',"").lower() == 'yes':
        url = "%s/" % url

    # Check to see if there is any content to transfer in the MetaDoc.
    if m.has_content():
        # Do not want to send any data if we're doing a dry run.
        if not dryrun:
            cli = metahttp.XMLClient(url, conf['key'], conf['cert'])

        if verbose:
            print "-" * 70
            print "Connecting to host: %s" % url
            print "Using key: %s" % conf['key']
            print "Using certificate: %s" % conf['cert']
            print "-" * 70
            print "Sent data:\n%s" % ("-" * 70)
            print m.get_xml(pretty=True)

        # Will not recieve any data on a dry run.
        if not dryrun:
            try:
                res = cli.send(m.get_xml())
            except (urllib2.HTTPError, urllib2.URLError) as httperror:
                logging.error(("Unable to connect to server address \"%s\". "
                    "Error: %s") % (url, httperror))
                # Since we're unable to send the document to the server, we will 
                # cache it so that we can send it at a later date.
                Cacher(element.xml_tag_name, m)
            else:
                if res:
                    xml_data = res.read()
                    if verbose:
                        print "%s\nRecieved data:\n%s" % ("-" * 70, "-" * 70)
                        print xml_data
                        print "-" * 70
                    utils.check_response(element.xml_tag_name, m, xml_data)
                else:
                    logging.error(("Server returned an empty response when "
                        "attempting to send \"%s\". Caching data.") % 
                        element.xml_tag_name)
                    # Since we recieved an empty response from the server we have 
                    # not recieved any reciept for any elements and must cache
                    # them.
                    Cacher(element.xml_tag_name, m)
    else:
        if verbose and not cache_only:
            print "No data to send for \"%s\"." % element.xml_tag_name
        logging.info(("No data to send for \"%s\".") % element.xml_tag_name)

def main():
    optstr = "hvqecaspunl:"
    optlist = ['help', 'dry-run', 'loglevel=', 'no-cache']
    SCRIPT_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
    # Default settings
    # Will be altered depending on passed options
    verbose = False
    dryrun = False
    send_cache = True
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
            a = StringIO.StringIO()
            sys.stdout = a
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

    log_file = datetime.datetime.strftime(datetime.datetime.now(), 
                "/var/log/mapi/metadoc.client.%Y-%m-%d.log")
    # Might get an error due to not having access to log directory.
    try:
        logging.basicConfig(level=log_level, 
            format=LOG_FORMAT,
            datefmt="%Y-%m-%d %H:%M:%S",
            filename=log_file 
            )
    except IOError, ioerr:
        print "Unable to open log file for writing, please check permissions"
        print "for %s" % log_file
        print "Error message: %s" % ioerr
        sys.exit(2)
    

    conf = ConfigParser.ConfigParser()
    conf.read("%s/%s" % (SCRIPT_PATH, "metadoc.conf"))
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
        # testConfig() prints/logs any errors
        return

    # ready for main processing.
    logging.info("Running main.py with handles %s." % " ".join(sys.argv[1:]))
    # Loading DTD for validation
    dtd_file = open("%s/%s" % (SCRIPT_PATH, "MetaDoc.dtd"), "r")
    dtd = lxml.etree.DTD(dtd_file)

    for element in send_elements:
        send_element(element, vals, send_cache, dryrun, verbose, False)

    # Checking if we have any cached items that should be sent
    for element in possible_send_elements:
        send_element(element, vals, send_cache, dryrun, verbose, True)
        

    for element in fetch_elements:
        url = "%s%s" % (vals['host'], element.url)
        cli = metahttp.XMLClient(url, vals['key'], vals['cert'])
        if verbose:
            print "-" * 70
            print "Connecting to host: %s" % url
            print "Using key: %s" % vals['key']
            print "Using certificate: %s" % vals['cert']
            print "-" * 70
        try:
            res = cli.send()
        except (urllib2.HTTPError, urllib2.URLError) as httperror:
            logging.error(("Unable to connect to server address \"%s\", "
                        "error: %s") % (url, httperror))
        else:
            if res:
                xml_data = res.read()
                if verbose:
                    print "%s\nRecieved data:\n%s" % ("-" * 70, "-" * 70)
                    print xml_data
                try:
                    return_data = lxml.etree.fromstring(xml_data)
                except lxml.etree.XMLSyntaxError, e:
                    logging.error(("Error parsing XML document from server: "
                                        "%s") % e)
                else:
                    # Check for valid according to DTD:
                    valid = dtd.validate(return_data)
                    if valid:
                        utils.check_version(return_data.attrib.get("version"))
                        found_elements = return_data.findall(
                                        element.xml_tag_name
                                        )
                        sub_elements = []
                        for found_element in found_elements:
                            sub_elements.append(MetaElement.from_xml_element(
                                                found_element, element)
                                                )
                        element.update_handler(sub_elements).process()
                    else:
                        logging.error(("XML recieved for \"%s\" did not "
                                    "contain valid XML according to DTD.") % 
                                    element.xml_tag_name)
                        dtd_errors = ""
                        for error in dtd.error_log.filter_from_errors():
                            dtd_errors = "%s\n%s" % (dtd_errors, error)
                        logging.debug("XML DTD errors: %s" % dtd_errors)
            else:
                logging.error(("Recieved empty response from server when "
                        "attempting to fetch \"%s\".") % element.xml_tag_name)


if __name__ == "__main__":
    main()
