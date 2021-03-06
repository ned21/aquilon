#!/usr/bin/env python
# -*- cpy-indent-level: 4; indent-tabs-mode: nil -*-
# ex: set expandtab softtabstop=4 shiftwidth=4:
#
# Copyright (C) 2008,2009,2010,2012,2013,2015,2016,2017,2018  Contributor
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Module for testing the update rack command."""

import unittest

if __name__ == "__main__":
    import utils
    utils.import_depends()

from brokertest import TestBrokerCommand


class TestUpdateRack(TestBrokerCommand):

    def test_010_verifyupdateut9(self):
        command = "show rack --rack ut9"
        out = self.commandtest(command.split(" "))
        self.matchoutput(out, "Rack: ut9", command)
        self.matchoutput(out, "Fullname: Aperture_name", command)
        self.matchoutput(out, "Row: g", command)
        self.matchoutput(out, "Column: 3", command)

    # Was row zz column 99
    def test_015_updatenp997(self):
        self.noouttest(["update", "rack", "--rack", "np997", "--row", "xx",
                        "--column", "77", "--fullname", "My Other Rack",
                        "--comments", "New other rack comments"])

    def test_020_verifyupdatenp997(self):
        command = "show rack --rack np997"
        out = self.commandtest(command.split(" "))
        self.matchoutput(out, "Rack: np997", command)
        self.matchoutput(out, "Fullname: My Other Rack", command)
        self.matchoutput(out, "Row: xx", command)
        self.matchoutput(out, "Column: 77", command)
        self.matchoutput(out, "Comments: New other rack comments", command)

    # Was row yy column 88
    def test_025_updatenp998(self):
        self.noouttest(["update", "rack", "--rack", "np998", "--row", "vv",
                        "--column", "66", "--fullname", "My Other Rack"])

    def test_030_failrow(self):
        command = ["update", "rack", "--rack", "np999", "--row", "a-b"]
        err = self.badrequesttest(command)
        self.matchoutput(err, "must be alphanumeric", command)

    def test_035_alphacolumn(self):
        """ we now accept characters for rack columns   """
        command = ["update", "rack", "--rack", "np999", "--column", "a"]
        self.noouttest(command)

    def test_100_prepare_CM_setup(self):
        command = ["update", "machine", "--machine", "ut9s03p41", "--rack", "ut8"] + self.valid_just_tcm
        self.noouttest(command)
        command = "search host --machine ut9s03p41"
        out = self.commandtest(command.split(" "))
        self.matchoutput(out, "aquilon91.aqd-unittest.ms.com", command)
        command = "show host --host aquilon91.aqd-unittest.ms.com"
        out = self.commandtest(command.split(" "))
        self.matchoutput(out, 'Environment: prod',
                         command)
        self.matchoutput(out, 'Build Status: ready',
                         command)
        self.matchoutput(out, 'Rack: ut8',
                         command)

    def test_105_updateroom(self):
        command = ['update_rack', '--rack=ut8', '--room=utroom1']
        self.justificationmissingtest(command, auth=True, msgcheck=False)

        command = ['update_rack', '--rack=ut8', '--room=utroom1'] + self.valid_just_tcm
        self.noouttest(command)

    def test_110_verifyroom(self):
        command = ['show_rack', '--rack=ut8']
        out = self.commandtest(command)
        self.searchoutput(out,
                          r'Location Parents: \[.*Building ut, Room utroom1\]',
                          command)

    def test_120_swaproom(self):
        command = ['update_rack', '--rack=ut8', '--room=utroom2']
        self.justificationmissingtest(command, auth=True, msgcheck=False)

        command = ['update_rack', '--rack=ut8', '--room=utroom2'] + self.valid_just_tcm
        self.noouttest(command)

    def test_130_verifyroom(self):
        command = ['show_rack', '--rack=ut8']
        out = self.commandtest(command)
        self.searchoutput(out,
                          r'Location Parents: \[.*Building ut, Room utroom2\]',
                          command)

    def test_140_updatebunker(self):
        command = ['update_rack', '--rack=ut8', '--bunker=bucket2.ut']
        self.justificationmissingtest(command, auth=True, msgcheck=False)

        command = ['update_rack', '--rack=ut8', '--bunker=bucket2.ut'] + self.valid_just_tcm
        self.noouttest(command)

    def test_145_verifybunker(self):
        command = ['show_rack', '--rack=ut8']
        out = self.commandtest(command)
        self.searchoutput(out,
                          r'Location Parents: \[.*Building ut, '
                          r'Room utroom2, Bunker bucket2.ut\]',
                          command)

    def test_150_clearroom(self):
        command = ['update_rack', '--rack=ut8', '--building', 'ut']
        self.justificationmissingtest(command, auth=True, msgcheck=False)

        command = ['update_rack', '--rack=ut8', '--building', 'ut'] + self.valid_just_sn
        self.noouttest(command)

    def test_160_verifyclear(self):
        command = ['show_rack', '--rack=ut8']
        out = self.commandtest(command)
        self.searchclean(out, r'Location Parents: \[.* Room .*\]', command)
        self.searchclean(out, r'Location Parents: \[.* Bunker .*\]', command)

    def test_170_failchangebuilding(self):
        command = ['update_rack', '--rack=ut8', '--room=np-lab1'] + self.valid_just_sn
        out = self.badrequesttest(command)
        self.matchoutput(out,
                         "Cannot change buildings.  Room np-lab1 is in "
                         "Building np while Rack ut8 is in Building ut.",
                         command)

    # Was row a column 3
    def test_180_updateut3(self):
        self.noouttest(["update", "rack", "--rack", "ut3", "--row", "b"])

    # Was row g column 2
    def test_185_updateut8(self):
        self.justificationmissingtest(["update", "rack", "--rack", "ut8", "--column", "8"],
                                      auth=True, msgcheck=False)

    # Was row g column 2
    def test_186_updateut8(self):
        self.emergencynojustification(["update", "rack", "--rack", "ut8", "--column", "8"] + self.emergency_just_with_reason)

    # Was row g column 3
    def test_190_updateut9(self):
        self.noouttest(["update", "rack", "--rack", "ut9", "--row", "h",
                        "--column", "9", "--fullname", "My Rack",
                        "--comments", "New rack comments"] + self.valid_just_sn)

    def test_195_verifyut9(self):
        command = "show rack --rack ut9"
        out = self.commandtest(command.split(" "))
        self.matchoutput(out, "Rack: ut9", command)
        self.matchoutput(out, "Fullname: My Rack", command)
        self.matchoutput(out, "Row: h", command)
        self.matchoutput(out, "Column: 9", command)
        self.matchoutput(out, "Comments: New rack comments", command)

    def test_200_defaultdns(self):
        command = ["update", "rack", "--rack", "ut9",
                   "--default_dns_domain", "aqd-unittest.ms.com"]
        self.noouttest(command)

    def test_210_verify_defaultdns(self):
        command = ["show", "rack", "--rack", "ut9"]
        out = self.commandtest(command)
        self.matchoutput(out, "Default DNS Domain: aqd-unittest.ms.com",
                         command)

    def test_220_clear_defaultdns(self):
        command = ["update", "rack", "--rack", "ut9",
                   "--default_dns_domain", ""]
        self.noouttest(command)

    def test_230_verify_defaultdns_gone(self):
        command = ["show", "rack", "--rack", "ut9"]
        out = self.commandtest(command)
        self.matchclean(out, "Default DNS", command)

    def test_235_search_fullname(self):
        command = ["search", "rack", "--fullname", "My Other Rack"]
        out = self.commandtest(command)
        self.matchoutput(out, "np997", command)
        self.matchoutput(out, "np998", command)

    def test_240_dsdb_fail(self):
        command = ["update", "rack", "--rack", "oy604",
                   "--comments", "Important comments"]
        out, err = self.successtest(command)
        self.matchoutput(err, "Rack oy604 update in DSDB failed!", command)
        self.matchoutput(err, "Update rack oy604 in DSDB failed, proceeding in AQDB.", command)

    def test_245_dsdb_fail_verify(self):
        command = ["show", "rack", "--rack", "oy604"]
        out = self.commandtest(command)
        self.matchoutput(out, "Comments: Important comments", command)


    def test_250_verifyshowallcsv(self):
        command = "show rack --all --format=csv"
        out = self.commandtest(command.split(" "))
        self.matchoutput(out, "rack,ut3,bunker,zebrabucket.ut,b,3,,ut3", command)
        self.matchoutput(out, "rack,ut8,building,ut,g,8", command)
        self.matchoutput(out, "rack,ut9,bunker,bucket2.ut,h,9", command)
        self.matchoutput(out, "rack,np997,building,np,xx,77", command)
        self.matchoutput(out, "rack,np998,building,np,vv,66", command)
        self.matchoutput(out, "rack,np999,building,np,zz,a", command)

    def test_255_verifyut3plenary(self):
        command = "cat --machine ut3c1n3"
        out = self.commandtest(command.split(" "))
        self.matchoutput(out, '"rack/name" = "ut3";', command)
        self.matchoutput(out, '"rack/row" = "b";', command)
        self.matchoutput(out, '"rack/column" = "3";', command)

    def test_300_verifyut8plenary(self):
        command = "cat --machine ut8s02p1"
        out = self.commandtest(command.split(" "))
        self.matchoutput(out, '"rack/name" = "ut8";', command)
        self.matchoutput(out, '"rack/row" = "g";', command)
        self.matchoutput(out, '"rack/column" = "8";', command)

    def test_355_verifyut9plenary(self):
        command = "cat --machine ut9s03p1"
        out = self.commandtest(command.split(" "))
        self.matchoutput(out, '"rack/name" = "ut9";', command)
        self.matchoutput(out, '"rack/row" = "h";', command)
        self.matchoutput(out, '"rack/column" = "9";', command)
        self.matchoutput(out, '"sysloc/room" = "utroom2";', command)
        self.matchoutput(out, '"sysloc/bunker" = "bucket2.ut";', command)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUpdateRack)
    unittest.TextTestRunner(verbosity=2).run(suite)
