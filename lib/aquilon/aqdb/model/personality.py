# -*- cpy-indent-level: 4; indent-tabs-mode: nil -*-
# ex: set expandtab softtabstop=4 shiftwidth=4:
#
# Copyright (C) 2009,2010,2011,2012,2013,2014  Contributor
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
""" Personality as a high level cfg object """
from datetime import datetime
import re

from sqlalchemy import (Column, Integer, Boolean, DateTime, Sequence, String,
                        ForeignKey, UniqueConstraint, PrimaryKeyConstraint)
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import relation, backref, deferred, object_session
from sqlalchemy.orm.collections import column_mapped_collection

from aquilon.exceptions_ import ArgumentError
from aquilon.aqdb.column_types import AqStr, Enum
from aquilon.aqdb.model import (Base, Archetype, Grn, HostEnvironment,
                                User, NetGroupWhiteList)

_TN = 'personality'
_PGN = 'personality_grn_map'
_PRU = 'personality_rootuser'
_PRNG = 'personality_rootnetgroup'
_PS = 'personality_stage'
_ALLOWED_STAGES = ('previous', 'current', 'next')


class Personality(Base):
    """ Personality names """
    __tablename__ = _TN

    id = Column(Integer, Sequence('%s_id_seq' % _TN), primary_key=True)
    name = Column(AqStr(64), nullable=False)
    archetype_id = Column(ForeignKey(Archetype.id), nullable=False)

    cluster_required = Column(Boolean(name="%s_clstr_req_ck" % _TN),
                              default=False, nullable=False)

    config_override = Column(Boolean(name="%s_config_override_ck" % _TN),
                             default=False, nullable=False)

    owner_eon_id = Column(ForeignKey(Grn.eon_id, name='%s_owner_grn_fk' % _TN),
                          nullable=False)

    host_environment_id = Column(ForeignKey(HostEnvironment.id), nullable=False)

    creation_date = deferred(Column(DateTime, default=datetime.now,
                                    nullable=False))
    comments = Column(String(255), nullable=True)

    archetype = relation(Archetype, innerjoin=True)
    owner_grn = relation(Grn, innerjoin=True)

    host_environment = relation(HostEnvironment, innerjoin=True)

    __table_args__ = (UniqueConstraint(archetype_id, name),
                      {'info': {'unique_fields': ['name', 'archetype']}},)

    def __init__(self, name=None, **kwargs):
        name = AqStr.normalize(name)
        super(Personality, self).__init__(name=name, **kwargs)

    @property
    def is_cluster(self):
        return self.archetype.cluster_type is not None

    @property
    def qualified_name(self):
        return self.archetype.name + "/" + self.name

    @classmethod
    def validate_env_in_name(cls, name, host_environment):
        env_mapper = inspect(HostEnvironment)
        persona_env = re.search("[-/](" +
                                "|".join(env_mapper.polymorphic_map) +
                                ")$", name, re.IGNORECASE)
        if persona_env and (persona_env.group(1) != host_environment):
            raise ArgumentError("Environment value in personality name '{0}' "
                                "does not match the host environment '{1}'"
                                .format(name, host_environment))

    @property
    def default_stage(self):
        """
        Return the default stage to be used for non-update operations
        """
        return self.stages["current"]

    @property
    def active_stage(self):
        """
        Return the default stage to be used for updates
        """
        return self.stages["current"]


class PersonalityStage(Base):
    __tablename__ = _PS
    _class_label = "Personality"

    id = Column(Integer, Sequence('%s_id_seq' % _PS), primary_key=True)

    personality_id = Column(ForeignKey(Personality.id, ondelete='CASCADE'),
                            nullable=False)
    name = Column(Enum(8, _ALLOWED_STAGES), nullable=False)

    # The plenary classes need the ORM to be aware if the object is deleted, so
    # we're using a ORM cascading instead of passive_deletes=True here.
    personality = relation(Personality, innerjoin=True,
                           backref=backref('stages',
                                           cascade='all, delete-orphan',
                                           collection_class=column_mapped_collection(name)))

    __table_args__ = (UniqueConstraint(personality_id, name,
                                       name='%s_uk' % _PS),)

    @property
    def qualified_name(self):
        return self.personality.qualified_name + "@" + self.name

    @property
    def cluster_required(self):
        return self.personality.cluster_required

    @property
    def owner_eon_id(self):
        return self.personality.owner_eon_id

    @property
    def archetype(self):
        return self.personality.archetype

    @property
    def owner_grn(self):
        return self.personality.owner_grn

    @property
    def host_environment(self):
        return self.personality.host_environment

    @property
    def root_users(self):
        return self.personality.root_users

    @property
    def root_netgroups(self):
        return self.personality.root_netgroups

    # FIXME: Drop this property when features are staged
    @property
    def features(self):
        return self.personality.features

    # FIXME: Drop this property when cluster_infos is staged
    @property
    def cluster_infos(self):
        return self.personality.cluster_infos

    def copy(self, name="current"):
        session = object_session(self)

        new = self.__class__(name=name)

        with session.no_autoflush:
            if self.paramholder:
                new.paramholder = self.paramholder.copy()
                new.paramholder.parameters.extend(param.copy()
                                                  for param in self.paramholder.parameters)

            new.services.extend(self.services)
            new.grns.extend(grn_link.copy() for grn_link in self.grns)

        return new

class PersonalityGrnMap(Base):
    __tablename__ = _PGN

    personality_stage_id = Column(ForeignKey(PersonalityStage.id,
                                             ondelete='CASCADE'),
                                  nullable=False)

    eon_id = Column(ForeignKey(Grn.eon_id), nullable=False)

    target = Column(AqStr(32), nullable=False)

    grn = relation(Grn, lazy=False, innerjoin=True)

    __table_args__ = (PrimaryKeyConstraint(personality_stage_id, eon_id,
                                           target),)

    def copy(self):
        return type(self)(eon_id=self.eon_id, target=self.target)

PersonalityStage.grns = relation(PersonalityGrnMap,
                                 cascade='all, delete-orphan',
                                 passive_deletes=True)


class __PersonalityRootUser(Base):
    __tablename__ = _PRU

    personality_id = Column(ForeignKey(Personality.id, ondelete='CASCADE'),
                            nullable=False)

    user_id = Column(ForeignKey(User.id, ondelete='CASCADE'), nullable=False)

    creation_date = deferred(Column(DateTime, default=datetime.now,
                                    nullable=False))

    __table_args__ = (PrimaryKeyConstraint(personality_id, user_id),)

Personality.root_users = relation(User,
                                  secondary=__PersonalityRootUser.__table__,
                                  passive_deletes=True)


class __PersonalityRootNetGroup(Base):
    __tablename__ = _PRNG

    personality_id = Column(ForeignKey(Personality.id, ondelete='CASCADE'),
                            nullable=False)

    netgroup_id = Column(ForeignKey(NetGroupWhiteList.id, ondelete='CASCADE'),
                         nullable=False)

    creation_date = deferred(Column(DateTime, default=datetime.now,
                                    nullable=False))

    __table_args__ = (PrimaryKeyConstraint(personality_id, netgroup_id),)

Personality.root_netgroups = relation(NetGroupWhiteList,
                                      secondary=__PersonalityRootNetGroup.__table__,
                                      passive_deletes=True)
