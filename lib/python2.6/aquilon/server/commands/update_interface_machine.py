# ex: set expandtab softtabstop=4 shiftwidth=4: -*- cpy-indent-level: 4; indent-tabs-mode: nil -*-
#
# Copyright (C) 2008,2009,2010  Contributor
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
"""Contains the logic for `aq update interface --machine`."""


from aquilon.exceptions_ import ArgumentError, AquilonError
from aquilon.server.broker import BrokerCommand
from aquilon.server.dbwrappers.interface import (get_interface,
                                                 restrict_switch_offsets,
                                                 verify_port_group,
                                                 choose_port_group)
from aquilon.server.locks import lock_queue
from aquilon.server.templates.machine import PlenaryMachineInfo
from aquilon.server.processes import DSDBRunner
from aquilon.aqdb.model.network import get_net_id_from_ip
from aquilon.aqdb.model import FutureARecord, ReservedName, Machine


class CommandUpdateInterfaceMachine(BrokerCommand):

    required_parameters = ["interface", "machine"]

    def render(self, session, logger, interface, machine, mac, ip, boot,
               pg, autopg, comments, **arguments):
        """This command expects to locate an interface based only on name
        and machine - all other fields, if specified, are meant as updates.

        If the machine has a host, dsdb may need to be updated.

        The boot flag can *only* be set to true.  This is mostly technical,
        as at this point in the interface it is difficult to tell if the
        flag was unset or set to false.  However, it also vastly simplifies
        the dsdb logic - we never have to worry about a user trying to
        remove the boot flag from a host in dsdb.

        """

        dbhw_ent = Machine.get_unique(session, machine, compel=True)
        dbinterface = get_interface(session, interface, dbhw_ent, None)

        oldinfo = DSDBRunner.snapshot_hw(dbhw_ent)

        if arguments.get('hostname', None):
            # Hack to set an intial interface for an aurora host...
            dbhost = dbhw_ent.host
            if dbhost.archetype.name == 'aurora' and \
               dbhw_ent.primary_ip and not dbinterface.vlans[0].addresses:
                dbinterface.vlans[0].addresses.append(dbhw_ent.primary_ip)

        # We may need extra IP verification (or an autoip option)...
        # This may also throw spurious errors if attempting to set the
        # port_group to a value it already has.
        if pg is not None and dbinterface.port_group != pg.lower().strip():
            dbinterface.port_group = verify_port_group(
                dbinterface.hardware_entity, pg)
        elif autopg:
            dbinterface.port_group = choose_port_group(
                dbinterface.hardware_entity)

        if ip:
            if len(dbinterface.vlans[0].addresses) > 1:
                raise ArgumentError("{0} has multiple addresses, "
                                    "update_interface can't handle "
                                    "that.".format(dbinterface))

            dbnetwork = get_net_id_from_ip(session, ip)
            restrict_switch_offsets(dbnetwork, ip)

            if dbinterface.vlans[0].assignments:
                assignment = dbinterface.vlans[0].assignments[0]
                if assignment.dns_records:
                    assignment.dns_records[0].network = dbnetwork
                    assignment.dns_records[0].ip = ip
                    session.flush()
                    session.expire(assignment, ['dns_records'])
                assignment.ip = ip
            else:
                dbinterface.vlans[0].addresses.append(ip)

            # Fix up the primary name if needed
            if dbinterface.bootable and \
               dbinterface.interface_type == 'public' and \
               dbhw_ent.primary_name and isinstance(dbhw_ent.primary_name,
                                                    ReservedName):
                short = dbhw_ent.primary_name.name
                dbdns_domain = dbhw_ent.primary_name.dns_domain
                session.delete(dbhw_ent.primary_name)
                session.flush()
                session.expire(dbhw_ent)
                dbdns_rec = FutureARecord(name=short, dns_domain=dbdns_domain,
                                          ip=ip)
                session.add(dbdns_rec)
                dbhw_ent.primary_name = dbdns_rec

        if comments:
            dbinterface.comments = comments
        if boot:
            for i in dbinterface.hardware_entity.interfaces:
                if i == dbinterface:
                    i.bootable = True
                elif i.bootable:
                    i.bootable = False
                    session.add(i)

        #Set this mac address last so that you can update to a bootable
        #interface *before* adding a mac address. This is so the validation
        #that takes place in the interface class doesn't have to be worried
        #about the order of update to bootable=True and mac address
        if mac:
            dbinterface.mac = mac

        session.add(dbinterface)
        session.flush()
        session.refresh(dbinterface)
        session.refresh(dbhw_ent)

        plenary_info = PlenaryMachineInfo(dbhw_ent, logger=logger)
        key = plenary_info.get_write_key()
        try:
            lock_queue.acquire(key)
            plenary_info.write(locked=True)

            if dbhw_ent.host and dbhw_ent.host.archetype.name != "aurora":
                dsdb_runner = DSDBRunner(logger=logger)
                dsdb_runner.update_host(dbhw_ent, oldinfo)
        except AquilonError, err:
            plenary_info.restore_stash()
            raise ArgumentError(err)
        except:
            plenary_info.restore_stash()
            raise
        finally:
            lock_queue.release(key)
        return
