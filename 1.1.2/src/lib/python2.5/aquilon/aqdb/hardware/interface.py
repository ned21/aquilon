#!/ms/dist/python/PROJ/core/2.5.0/bin/python
# ex: set expandtab softtabstop=4 shiftwidth=4: -*- cpy-indent-level: 4; indent-tabs-mode: nil -*-
# $Header$
# $Change$
# $DateTime$
# $Author$
# Copyright (C) 2008 Morgan Stanley
#
# This module is part of Aquilon
"""Classes and Tables relating to network interfaces"""
import sys
sys.path.append('../..')

import os
import re
import datetime

from db import *
from aquilon import const

from sqlalchemy import (Column, Table, Integer, Sequence, String, Index,
                        Boolean, CheckConstraint, UniqueConstraint, DateTime,
                        ForeignKey, PrimaryKeyConstraint, insert, select )

from sqlalchemy.orm import mapper, relation, deferred

from interface_type import InterfaceType, interface_type
from location import Location, location,Chassis, chassis
from machine import Machine, machine
from configuration import CfgPath, cfg_path
from aquilon.exceptions_ import ArgumentError

interface = Table('interface',meta,
    Column('id', Integer, Sequence('interface_id_seq'), primary_key=True),
    Column('interface_type_id', Integer,
           ForeignKey('interface_type.id'), nullable=False),
    Column('ip',String(16), default='0.0.0.0', index=True),
    Column('creation_date', DateTime, default=datetime.now),
    Column('comments',String(255))) #TODO FK to IP table)
interface.create(checkfirst=True)

class Interface(aqdbBase):
    """ Base Class of various network interface structures """
    def __init__(self, name, *args,**kw):
        self.name = name.strip().lower()
        if (kw.has_key('ip')):
            self.ip = kw['ip']
        else:
            self.ip = ''

mapper(Interface,interface,
       polymorphic_on=interface.c.interface_type_id,
        polymorphic_identity=engine.execute(
           "select id from interface_type where type='base_interface_type'").\
            fetchone()[0], properties={
                        'type': relation(InterfaceType),
                        'creation_date' : deferred(interface.c.creation_date),
                        'comments': deferred(interface.c.comments)})

physical_interface=Table('physical_interface', meta,
    Column('interface_id', Integer,
           ForeignKey('interface.id', ondelete='CASCADE'), primary_key=True),
    Column('machine_id', Integer,
           ForeignKey('machine.id',ondelete='CASCADE'),
           nullable=False),
    Column('name',String(32), nullable=False), #like e0, hme1, etc.
    Column('mac', String(32), nullable=False),
    Column('boot', Boolean, default=False),
    UniqueConstraint('mac',name='mac_addr_uk'),
    UniqueConstraint('machine_id','name',name='phy_iface_uk'))
Index('idx_phys_int_machine_id', physical_interface.c.machine_id)
physical_interface.create(checkfirst=True)

class PhysicalInterface(Interface):
    """ Class to model up the physical nic cards/devices in machines """
    @optional_comments
    def __init__(self, name, mac, machine, *args,**kw):
        Interface.__init__(self, name, *args, **kw)
        self.name = name.strip().lower()
        self.mac  = mac.strip().lower()
        reg = re.compile('^([a-f0-9]{2,2}:){5,5}[a-f0-9]{2,2}$')
        if (not reg.match(self.mac)):
            raise ArgumentError ('Invalid MAC address: '+self.mac)
        self.machine= machine
        if kw.has_key('boot'):
            self.boot=kw.pop('boot')
        elif self.name == 'e0':
            self.boot=True
        #TODO: tighten this up with type/value checks
        #we should probably also constrain the name

mapper(PhysicalInterface, physical_interface,
       inherits=Interface, polymorphic_identity=engine.execute(
           "select id from interface_type where type='physical'").\
            fetchone()[0], properties={
    'machine'   : relation(Machine, backref='interfaces' ),
    'interface' : relation(Interface, lazy=False, backref='physical')})
    #collection_clas=attribute_mapped_collection('name'))})

#class NetworkLink(aqdbBase):
#    __tablename__ = 'network_link'



#if __name__ == '__main__':