#!/ms/dist/python/PROJ/core/2.5.0/bin/python
# ex: set expandtab softtabstop=4 shiftwidth=4: -*- cpy-indent-level: 4; indent-tabs-mode: nil -*-
# $Header$
# $Change$
# $DateTime$
# $Author$
# Copyright (C) 2008 Morgan Stanley
#
# This module is part of Aquilon
"""Contains the logic for `aq bind client`."""


from sqlalchemy.exceptions import InvalidRequestError

from aquilon.exceptions_ import ArgumentError
from aquilon.server.broker import (format_results, add_transaction, az_check,
                                   BrokerCommand)
from aquilon.aqdb.systems import BuildItem
from aquilon.server.dbwrappers.host import (hostname_to_host,
                                            get_host_build_item)
from aquilon.server.dbwrappers.service import get_service
from aquilon.server.dbwrappers.service_instance import (get_service_instance,
                                                        choose_service_instance)


class CommandBindClient(BrokerCommand):

    required_parameters = ["hostname", "service"]

    @add_transaction
    @az_check
    def render(self, session, hostname, service, instance, force=False,
            **arguments):
        dbhost = hostname_to_host(session, hostname)
        dbservice = get_service(session, service)
        if instance:
            dbinstance = get_service_instance(session, dbservice, instance)
        else:
            dbinstance = choose_service_instance(session, dbhost, dbservice)
        dbtemplate = get_host_build_item(session, dbhost, dbservice)
        if dbtemplate:
            if dbtemplate.cfg_path == dbinstance.cfg_path:
                # Already set - no problems.
                return
            if not force:
                raise ArgumentError("Host %s is already bound to %s, use unbind to clear first or rebind to force."
                        % (hostname, dbtemplate.cfg_path.relative_path))
            session.delete(dbtemplate)
        # FIXME: Should enforce that the instance has a server bound to it.
        positions = []
        session.flush()
        session.refresh(dbhost)
        for template in dbhost.templates:
            positions.append(template.position)
            if template.cfg_path == dbinstance:
                return
        # Do not bind to 0 (os) or 1 (personality)
        i = 2
        while i in positions:
            i += 1
        bi = BuildItem(dbhost, dbinstance.cfg_path, i)
        session.save(bi)
        session.flush()
        session.refresh(dbhost)
        return


#if __name__=='__main__':