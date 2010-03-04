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

import MetaHTTP
from MetaDoc import MetaDoc
from Users import Users
from Projects import Projects
from Allocations import Allocations
from Events import Events
from SiteInfo import SiteInfo
import ConfigParser

def write_sample_config():
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
    if 'valid' in vals:
        if vals['valid'].lower() == "false" or vals['valid'].lower() == "no":
            print "Config not valid. Please configure the program properly."
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
        return

    # ready for main processing.
    m = MetaDoc(True)
    u = Users()
    p = Projects()
    a = Allocations()
    e = Events("foo_site")
    si = SiteInfo('foo_site')

    # --------------------------------------------------------- #
    # Example entries, edit/change at will
    # --------------------------------------------------------- #
    u.addEntry(username='foo',
               full_name='Foo Bar',
               uid='1001',
               password="234",
               default_group="admins",
               special_path="/home",
               shell="/usr/bin/zsh",
               email="foo@example.org",
               status="new",
               phone="555-12345")
    u.addEntry(username='bar',
               password="xxyyzz",
               status="existing")
    u.addEntry(username='admin',
               status="delete")
    # users = ['foo', 'bar']
    # p.addEntry(name="Test-project",
    #            gid="123",
    #            status="existing",
    #            account_nmb="NN12345",
    #            valid_from="12-01-2010",
    #            usernames=users)
    # p.addEntry(name="Test-project2",
    #            gid="1232",
    #            status="new",
    #            account_nmb="NN12346",
    #            valid_from="12-01-2010",
    #            valid_to="12-01-2012",
    #            usernames=users)
    # a.addEntry("NN12345", "10000", "pri", "2010.1")
    # a.addEntry("NN12345", "10010", "nonpri", "2010.1")
    # a.addEntry("NN12345", "10010", "pri", "2010.2")
    # a.addEntry("NN12345", "10010", "nonpri", "2010.2")
    # e.addDown("run out of jet-fuel",
    #           "10-02-2010",
    #           "14-02-2010",
    #           "100",
    #           remarks="nothing special")
    # e.addUp("12-02-2010",
    #         remarks="especially nothing special")

    # si.addSW('gcc', '4.3.3', license="GPLv3", infoURL="http://www.google.com")
    # si.addConfig('cores', 'count', '100')

    # Register the elements witht he main documen.thttp://www.kernel.org/pub/software/scm/git/docs/RelNotes-1.6.6.txt
    m.regMetaElement(u)
    m.regMetaElement(p)
    m.regMetaElement(a)
    m.regMetaElement(e)
    m.regMetaElement(si)

    # Get ready to send the data
    cli = MetaHTTP.XML_Client(vals['host'], vals['key'], vals['cert'])
    res = cli.send(m.getXML())
    if res:
        print res.read()

if __name__ == "__main__":
    main()

