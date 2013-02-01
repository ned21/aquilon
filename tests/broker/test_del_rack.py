#!/usr/bin/env python2.6
# -*- cpy-indent-level: 4; indent-tabs-mode: nil -*-
# ex: set expandtab softtabstop=4 shiftwidth=4:
#
# Copyright (C) 2008,2009,2010,2011,2013  Contributor
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the EU DataGrid Software License.  You should
# have received a copy of the license with this program, and the
# license is published at
# http://eu-datagrid.web.cern.ch/eu-datagrid/license.html.
#
# THE FOLLOWING DISCLAIMER APPLIES TO ALL SOFTWARE CODE AND OTHER
# MATERIALS CONTRIBUTED IN CONNECTION WITH THIS PROGRAM.
#
# THIS SOFTWARE IS LICENSED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE AND ANY WARRANTY OF NON-INFRINGEMENT, ARE
# DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. THIS
# SOFTWARE MAY BE REDISTRIBUTED TO OTHERS ONLY BY EFFECTIVELY USING
# THIS OR ANOTHER EQUIVALENT DISCLAIMER AS WELL AS ANY OTHER LICENSE
# TERMS THAT MAY APPLY.
"""Module for testing the del rack command."""

import unittest

if __name__ == "__main__":
    import utils
    utils.import_depends()

from brokertest import TestBrokerCommand


class TestDelRack(TestBrokerCommand):

    def testdelut3(self):
        command = "del rack --rack ut3"
        self.noouttest(command.split(" "))

    def testverifydelut3(self):
        command = "show rack --rack ut3"
        self.notfoundtest(command.split(" "))

    def testdelnp3(self):
        command = "del rack --rack np3"
        self.noouttest(command.split(" "))

    def testdelut4(self):
        command = "del rack --rack ut4"
        self.noouttest(command.split(" "))

    def testdelnp997(self):
        command = "del rack --rack np997"
        self.noouttest(command.split(" "))

    def testverifydelnp997(self):
        command = "show rack --rack np997"
        self.notfoundtest(command.split(" "))

    # Created by test_add_tor_switch
    def testdelnp998(self):
        command = "del rack --rack np998"
        self.noouttest(command.split(" "))

    def testverifydelnp998(self):
        command = "show rack --rack np998"
        self.notfoundtest(command.split(" "))

    # Created by test_add_tor_switch
    def testdelnp999(self):
        command = "del rack --rack np999"
        self.noouttest(command.split(" "))

    def testverifydelnp999(self):
        command = "show rack --rack np999"
        self.notfoundtest(command.split(" "))

    # FIXME: Maybe del_tor_switch should remove the rack if it is
    # otherwise empty.
    def testdelut8(self):
        command = "del rack --rack ut8"
        self.noouttest(command.split(" "))

    def testverifydelut8(self):
        command = "show rack --rack ut8"
        self.notfoundtest(command.split(" "))

    def testdelut9(self):
        command = "del rack --rack ut9"
        self.noouttest(command.split(" "))

    def testverifydelut9(self):
        command = "show rack --rack ut9"
        self.notfoundtest(command.split(" "))

    def testdelcards(self):
        command = "del rack --rack cards1"
        self.noouttest(command.split(" "))

    def testverifyvards(self):
        command = "show rack --rack cards1"
        self.notfoundtest(command.split(" "))

    def testdelracknetwork(self):
        test_rack = "ut9"

        # add network to rack
        self.noouttest(["add_network", "--ip", "192.176.6.0",
                        "--network", "test_warn_network",
                        "--netmask", "255.255.255.0",
                        "--rack", test_rack,
                        "--type", "unknown",
                        "--comments", "Made-up network"])

        # try delete rack
        command = "del rack --rack %s" % test_rack
        err = self.badrequesttest(command.split(" "))
        self.matchoutput(err,
                         "Bad Request: Could not delete rack %s, networks "
                         "were found using this location." % test_rack,
                         command)

        # delete network
        self.noouttest(["del_network", "--ip", "192.176.6.0"])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDelRack)
    unittest.TextTestRunner(verbosity=2).run(suite)
