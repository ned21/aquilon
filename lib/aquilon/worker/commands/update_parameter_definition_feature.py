# -*- cpy-indent-level: 4; indent-tabs-mode: nil -*-
# ex: set expandtab softtabstop=4 shiftwidth=4:
#
# Copyright (C) 2009,2010,2011,2012,2013,2014,2015  Contributor
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


from aquilon.aqdb.model import Feature, FeatureParamDef, ParamDefinition
from aquilon.worker.broker import BrokerCommand  # pylint: disable=W0611
from aquilon.worker.dbwrappers.parameter import validate_param_definition


class CommandUpdParameterDefintionFeature(BrokerCommand):

    required_parameters = ["feature", "type", "path"]

    def render(self, session, feature, type, path, required,
               default, description, **kwargs):
        cls = Feature.polymorphic_subclass(type, "Unknown feature type")
        dbfeature = cls.get_unique(session, name=feature, compel=True)

        if not dbfeature.param_def_holder:
            dbfeature.param_def_holder = FeatureParamDef()

        db_paramdef = ParamDefinition.get_unique(session, path=path,
                                                 holder=dbfeature.param_def_holder,
                                                 compel=True)

        if default:
            validate_param_definition(db_paramdef.path, db_paramdef.value_type,
                                      default)
            db_paramdef.default = default

        if required is not None:
            db_paramdef.required = required
        if description is not None:
            db_paramdef.description = description

        session.flush()

        return
