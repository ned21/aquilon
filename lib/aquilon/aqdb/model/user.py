# -*- cpy-indent-level: 4; indent-tabs-mode: nil -*-
# ex: set expandtab softtabstop=4 shiftwidth=4:
#
# Copyright (C) 2008-2014,2018  Contributor
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
""" Class for maanaging User """

from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Sequence,
    String,
)
from sqlalchemy.orm import (
    deferred,
    relation,
)

from aquilon.aqdb.column_types import AqStr
from aquilon.aqdb.model import Base

_TYPES = 'user_type'
_TN = 'userinfo'


class UserType(Base):
    __tablename__ = _TYPES

    id = Column(Integer, Sequence('%s_id_seq' % __tablename__),
                primary_key=True)
    name = Column(AqStr(64), nullable=False, unique=True)

    creation_date = deferred(Column(DateTime, default=datetime.now,
                                    nullable=False))
    comments = Column(String(255), nullable=True)

    __table_args__ = ({'info': {'unique_fields': ['name']}},)


class User(Base):
    """ Manage Users  """
    __tablename__ = _TN
    _class_label = 'User'

    # Use a synthetic primary key, in case we will need to support multiple user
    # environments in the future
    id = Column(Integer, Sequence('%s_id_seq' % _TN), primary_key=True)

    # user names are case sensitive, so no AqStr here
    name = Column(String(32), nullable=False, unique=True)

    uid = Column(Integer, nullable=False, unique=True)
    gid = Column(Integer, nullable=False)
    full_name = Column(String(64), nullable=False)
    home_dir = Column(String(64), nullable=False)

    type_id = Column(ForeignKey(UserType.id), nullable=False)
    type = relation(UserType, lazy=False, innerjoin=True)

    creation_date = deferred(Column(DateTime, default=datetime.now,
                                    nullable=False))

    __table_args__ = ({'info': {'unique_fields': ['name']}},)
