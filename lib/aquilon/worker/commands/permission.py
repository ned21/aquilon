# -*- cpy-indent-level: 4; indent-tabs-mode: nil -*-
# ex: set expandtab softtabstop=4 shiftwidth=4:
#
# Copyright (C) 2008,2009,2010,2011,2013  Contributor
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
"""Contains the logic for `aq permission`."""


from aquilon.worker.broker import BrokerCommand  # pylint: disable=W0611
from aquilon.worker.dbwrappers.user_principal import (
    get_or_create_user_principal)
from aquilon.aqdb.model import Role


class CommandPermission(BrokerCommand):

    required_parameters = ["principal", "role"]

    def render(self, session, logger, principal, role, createuser, createrealm,
               comments, **arguments):
        dbrole = Role.get_unique(session, role, compel=True)
        dbuser = get_or_create_user_principal(session, principal, createuser,
                                              createrealm, comments=comments,
                                              logger=logger)
        dbuser.role = dbrole
        session.flush()
        return
