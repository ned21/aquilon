# -*- cpy-indent-level: 4; indent-tabs-mode: nil -*-
# ex: set expandtab softtabstop=4 shiftwidth=4:
#
# Copyright (C) 2013,2014,2015  Contributor
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
"""Contains the logic for `aq search personality`."""

from sqlalchemy.orm import joinedload, subqueryload, contains_eager
from sqlalchemy.sql import or_

from aquilon.aqdb.model import (Archetype, Personality, PersonalityStage,
                                HostEnvironment, PersonalityGrnMap, Service)
from aquilon.worker.broker import BrokerCommand
from aquilon.worker.dbwrappers.grn import lookup_grn
from aquilon.worker.formats.list import StringAttributeList


class CommandSearchPersonality(BrokerCommand):

    required_parameters = []

    def render(self, session, personality, archetype, grn, eon_id,
               host_environment, config_override, required_service, fullinfo,
               style, **arguments):
        q = session.query(PersonalityStage)
        q = q.join(Personality)
        if archetype:
            dbarchetype = Archetype.get_unique(session, archetype, compel=True)
            q = q.filter_by(archetype=dbarchetype)

        if personality:
            q = q.filter_by(name=personality)

        if config_override:
            q = q.filter_by(config_override=True)

        if host_environment:
            dbhost_env = HostEnvironment.get_instance(session, host_environment)
            q = q.filter_by(host_environment=dbhost_env)

        if grn or eon_id:
            dbgrn = lookup_grn(session, grn, eon_id, autoupdate=False,
                               usable_only=False)
            q = q.outerjoin(PersonalityStage, PersonalityGrnMap, aliased=True)
            q = q.filter(or_(Personality.owner_eon_id == dbgrn.eon_id,
                             PersonalityGrnMap.eon_id == dbgrn.eon_id))
            q = q.reset_joinpoint()

        if required_service:
            dbsrv = Service.get_unique(session, required_service, compel=True)
            q = q.filter(PersonalityStage.services.contains(dbsrv))

        q = q.join(Archetype)
        q = q.order_by(Archetype.name, Personality.name, PersonalityStage.name)
        q = q.options(contains_eager('personality'),
                      contains_eager('personality.archetype'))

        if fullinfo or style != 'raw':
            q = q.options(subqueryload('services'),
                          subqueryload('grns'),
                          # FIXME: Undo when feature bindings are staged
                          subqueryload('personality.features'),
                          joinedload('personality.features.feature'),
                          # FIXME: Undo when cluster_infos is staged
                          joinedload('personality.cluster_infos'))
            return q.all()
        else:
            return StringAttributeList(q.all(), "qualified_name")
