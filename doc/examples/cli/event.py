#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#            event.py is part of MetaDoc (Client).
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
"""Registers an event through a command line interface that can be sent 
through MetaDoc client.

main.py should be run afterwards in order to send data to server.

Usage:
--help                  Displays this help message.
--up                    Sets event type to resource up(1).
--down                  Sets event type to resource down(1).
--reason=<reason>       Sets the reason for the event(2)
--dateup=<date>         Sets the date for the system comming up(2,3).
--datedown=<date>       Sets the date for the system going down(2,3).
--sharedown=<share>     Sets the percentage of the system being down during 
                        the event(2).
--dateformat=<format>   Sets the format of the dates that are passed in python 
                        format(4)
--remarks=<file>        File path for a text file containing remarks. This may
                        be a longer description than reason.

(1) Either --up or --down must be passed.
(2) Required if --down is passed.
(3) Must follow <format>. If --dateformat is not passed, <format> is set to 
    "%Y-%m-%d %H:%M:%S"
(4) http://docs.python.org/library/datetime.html#strftime-and-strptime-behavior
"""
import getopt
import sys
from datetime import datetime

from events.definition import Events
from events.entries import ResourceUpEntry, ResourceDownEntry
from metadoc import MetaDoc
from cacher import Cacher

def main():
    optlist = ['help', 'up', 'down', 'reason=', 'dateup=', 'datedown=', 
                'sharedown=', 'dateformat=', 'remarks=']
    event_type = None
    reason = None
    date_up = datetime.now()
    date_down = datetime.now()
    share_down = None
    date_format = "%Y-%m-%d %H:%M:%S"
    remarks = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", optlist)
    except getopt.GetoptError, goe:
        print str(goe)
        print __doc__
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('--help'):
            print __doc__
            sys.exit()
        elif opt in ('--up'):
            event_type = "resourceUp"
        elif opt in ('--down'):
            event_type = "resourceDown"
        elif opt in ('--reason'):
            reason = arg
        elif opt in ('--dateup'):
            date_up = arg
        elif opt in ('--datedown'):
            date_down = arg
        elif opt in ('--sharedown'):
            share_down = arg
        elif opt in ('--dateformat'):
            date_format = arg
        elif opt in ('--remarks'):
            try:
                rfile = open(arg, "r")
            except IOError, e:
                print "Could not open file containing remarks."
                print "Got error: %s" % str(e)
                print "Halting."
                sys.exit(2)
            else:
                remarks = rfile.read()
                rfile.close()

    if not isinstance(date_up, datetime):
        if date_up is not None:
            try:
                date_up = datetime.strptime(date_up, date_format)
            except ValueError, e:
                print "Date up recieved, but format does not match."
                print str(e)
                print __doc__
                sys.exit(2)
    if not isinstance(date_down, datetime):
        if date_down is not None:
            try:
                date_down = datetime.strptime(date_down, date_format)
            except ValueError, e:
                print "Date down recieved, but format does not match."
                print str(e)
                print __doc__
                sys.exit(2)
    if event_type is None:
        print "Missing event type."
        print __doc__
        sys.exit(2)
    else:
        if event_type == "resourceDown":
            if reason is None:
                print "Recieved resource down handle, but missing reason."
                print __doc__
                sys.exit(2)
            if share_down is None:
                print "Recieved resource down handle, but missing share down."
                print __doc__
                sys.exit(2)
    # We have everything we require to create an event.
    # Attempt to find already cached data:
    m = MetaDoc(True)
    c = Cacher("events")
    cached_data = c.get_cache()
    if cached_data is not None:
        processor = Events.from_xml_element(cached_data, Events)
        if processor is None:
            print "Found previous event cache, but could not load. Please check "
            print "\"%s\" for errors. " % c.file_path
            print "Halting."
            sys.exit(2)
        else:
            c.remove_cache()
    else:
        processor = Events()
    if event_type == "resourceUp":
        e = ResourceUpEntry(date_up, reason, remarks)
    else:
        e = ResourceDownEntry(reason, date_down, date_up, share_down, remarks)
    processor.add_element(e)
    m.reg_meta_element(processor)
    Cacher(Events.xml_tag_name, m)
    print "Event has been registered. Run main.py to send to server."

if __name__=='__main__':
    main()
