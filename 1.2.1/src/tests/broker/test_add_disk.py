#!/ms/dist/python/PROJ/core/2.5.0/bin/python
# ex: set expandtab softtabstop=4 shiftwidth=4: -*- cpy-indent-level: 4; indent-tabs-mode: nil -*-
# $Header$
# $Change$
# $DateTime$
# $Author$
# Copyright (C) 2008 Morgan Stanley
#
# This module is part of Aquilon
"""Module for testing the add disk command."""

import os
import sys
import unittest

if __name__ == "__main__":
    BINDIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    SRCDIR = os.path.join(BINDIR, "..", "..")
    sys.path.append(os.path.join(SRCDIR, "lib", "python2.5"))

from brokertest import TestBrokerCommand


class TestAddDisk(TestBrokerCommand):

    def testaddut3c5n10disk(self):
        self.noouttest(["add", "disk", "--machine", "ut3c5n10",
            "--type", "scsi", "--capacity", "34"])

    def testverifyaddut3c5n10disk(self):
        command = "show machine --machine ut3c5n10"
        out = self.commandtest(command.split(" "))
        self.matchoutput(out, "Disk: 34 GB scsi", command)

    # Note: This test should probably be improved, or maybe actually fix
    # the underlying problem in the server.  The plenary templates only
    # write out information for the first disk.  Since this is an hs21,
    # the model includes a 68 GB disk, which was added when the host was
    # created.  This can most likely only be fixed after AQUILONAQD-65 is
    # resolved.
    def testverifycatut3c5n10disk(self):
        command = "cat --machine ut3c5n10"
        out = self.commandtest(command.split(" "))
        self.matchoutput(out,
                """"harddisks" = nlist("sda", create("hardware/harddisk/generic/scsi", "capacity", 68*GB));""",
                command)

    def testaddut3c1n3disk(self):
        self.noouttest(["add", "disk", "--machine", "ut3c1n3",
            "--type", "scsi", "--capacity", "34"])

    def testverifyaddut3c1n3disk(self):
        command = "show machine --machine ut3c1n3"
        out = self.commandtest(command.split(" "))
        self.matchoutput(out, "Disk: 34 GB scsi", command)

    # See note on testverifycatut3c5n10disk(), above.
    def testverifycatut3c1n3disk(self):
        command = "cat --machine ut3c1n3"
        out = self.commandtest(command.split(" "))
        self.matchoutput(out,
                """"harddisks" = nlist("sda", create("hardware/harddisk/generic/scsi", "capacity", 68*GB));""",
                command)


if __name__=='__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAddDisk)
    unittest.TextTestRunner(verbosity=2).run(suite)
