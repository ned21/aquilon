#!/usr/bin/env python2.5
# ex: set expandtab softtabstop=4 shiftwidth=4: -*- cpy-indent-level: 4; indent-tabs-mode: nil -*-
#
# Copyright (C) 2008,2009  Contributor
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
""" tests create and delete of a machine through the session """
import unittest
from utils import load_classpath, add, commit

load_classpath()

import aquilon.aqdb.depends
from aquilon.aqdb.db_factory import DbFactory
from aquilon.aqdb.model import Vendor, Model, Machine, Cpu, Rack

db = DbFactory()
sess = db.Session()
NAME = ''
VENDOR='hp'
MODEL='bl45p'

def setUp():


    t = sess.query(Machine).filter_by(name = NAME).first()
    if t is not None:
        sess.delete(t)
        sess.commit()

def tearDown():
    #TODO: this is a recursive definition. Fix it with a direct sql statement later on
    if len(sess.query(Machine).filter_by(name = NAME).all()) > 0:
        testDelMachine()

def testInitMachine():
    vnd = sess.query(Vendor).filter_by(name=VENDOR).one()
    assert vnd, "Can't find vendor %s"%(VENDOR)

    mdl  = sess.query(Model).filter_by(name=MODEL).one()
    assert mdl, "Can't find model %s"%(MODEL)

    proc = sess.query(Cpu).first()
    assert proc, "Can't find a cpu"

    rack = sess.query(Rack).first()
    assert rack, "Can't find a rack"

    NAME = rack.name + 'c1n3'
    mchn = Machine(name=NAME, model=mdl, location=rack, cpu=proc)

    add(sess, mchn)
    commit(sess)

    assert mchn, 'Commit machine failed'
    print mchn

def testDelMachine():
    mchn = sess.query(Machine).filter_by(name = NAME).first()
    if mchn:
        s.delete(mchn)
        commit(sess)

        t = sess.query(Machine).filter_by(name = NAME).first()
        assert t is None
        print 'deleted machine'

