# -*- cpy-indent-level: 4; indent-tabs-mode: nil -*-
# ex: set expandtab softtabstop=4 shiftwidth=4:
#
# Copyright (C) 2008,2009,2010,2011,2012,2013  Contributor
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
"""Contains the logic for `aq map service`."""

from aquilon.exceptions_ import ArgumentError
from aquilon.worker.broker import BrokerCommand  # pylint: disable=W0611
from aquilon.aqdb.model import (Personality, Service, ServiceMap,
                                 PersonalityServiceMap,
                                NetworkEnvironment)
from aquilon.worker.dbwrappers.location import get_location
from aquilon.worker.dbwrappers.service_instance import get_service_instance
from aquilon.worker.dbwrappers.network import get_network_byip


class CommandMapService(BrokerCommand):

    required_parameters = ["service", "instance"]

    def render(self, session, service, instance, archetype, personality,
               networkip, **kwargs):

        dbservice = Service.get_unique(session, service, compel=True)
        dblocation = get_location(session, **kwargs)
        dbinstance = get_service_instance(session, dbservice, instance)

        if networkip:
            dbnet_env = NetworkEnvironment.get_unique_or_default(session)
            dbnetwork = get_network_byip(session, networkip, dbnet_env)
        else:
            dbnetwork = None

        if archetype is None and personality:
            # Can't get here with the standard aq client.
            raise ArgumentError("Specifying --personality requires you to "
                                "also specify --archetype.")

        kwargs = {}
        if archetype and personality:
            dbpersona = Personality.get_unique(session, name=personality,
                                               archetype=archetype, compel=True)

            map_class = PersonalityServiceMap
            query = session.query(map_class).filter_by(personality=dbpersona)

            kwargs["personality"] = dbpersona
        else:
            map_class = ServiceMap
            query = session.query(map_class)

        dbmap = query.filter_by(location=dblocation,
                                service_instance=dbinstance,
                                network=dbnetwork).first()

        if not dbmap:
            dbmap = map_class(service_instance=dbinstance,
                              location=dblocation,
                              network=dbnetwork, **kwargs)

        session.add(dbmap)
        session.flush()

        return
