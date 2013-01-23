# -*- cpy-indent-level: 4; indent-tabs-mode: nil -*-
# ex: set expandtab softtabstop=4 shiftwidth=4:
#
# Copyright (C) 2008,2009,2010,2011,2012  Contributor
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

from aquilon.aqdb.model import ARecord
from aquilon.worker.broker import BrokerCommand
from aquilon.worker.dbwrappers.dns import grab_address
from aquilon.worker.dbwrappers.interface import generate_ip
from aquilon.worker.processes import DSDBRunner


class CommandAddAddressDNSEnvironment(BrokerCommand):

    required_parameters = ["fqdn", "dns_environment"]

    def render(self, session, logger, fqdn, dns_environment,
               network_environment, reverse_ptr, comments, **arguments):

        ip = generate_ip(session, compel=True, dbinterface=None,
                         network_environment=network_environment, **arguments)
        # TODO: add allow_multi=True
        dbdns_rec, newly_created = grab_address(session, fqdn, ip,
                                                network_environment,
                                                dns_environment,
                                                comments=comments,
                                                preclude=True)

        if reverse_ptr:
            # Technically the reverse PTR could point to other types, not just
            # ARecord, but there are no use cases for that, so better avoid
            # confusion
            dbreverse = ARecord.get_unique(session, fqdn=reverse_ptr,
                                           dns_environment=dns_environment,
                                           compel=True)
            if dbreverse.fqdn != dbdns_rec.fqdn:
                dbdns_rec.reverse_ptr = dbreverse.fqdn

        session.flush()

        if dbdns_rec.fqdn.dns_environment.is_default:
            dsdb_runner = DSDBRunner(logger=logger)
            dsdb_runner.add_host_details(dbdns_rec.fqdn, ip, comments=comments)
            dsdb_runner.commit_or_rollback("Could not add address to DSDB")

        return
