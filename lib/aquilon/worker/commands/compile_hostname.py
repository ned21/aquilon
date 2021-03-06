# -*- cpy-indent-level: 4; indent-tabs-mode: nil -*-
# ex: set expandtab softtabstop=4 shiftwidth=4:
#
# Copyright (C) 2008-2013,2015-2016,2019  Contributor
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
"""Contains the logic for `aq compile`."""

from aquilon.worker.broker import BrokerCommand
from aquilon.worker.dbwrappers.host import hostname_to_host
from aquilon.worker.templates import Plenary, TemplateDomain


class CommandCompileHostname(BrokerCommand):

    required_parameters = ["hostname"]
    requires_readonly = True

    def render_old(self, session, logger, hostname, pancinclude, pancexclude,
               pancdebug, cleandeps, **_):
        dbhost = hostname_to_host(session, hostname)
        if pancdebug:
            pancinclude = r'.*'
            pancexclude = r'components/spma/functions.*'
        dom = TemplateDomain(dbhost.branch, dbhost.sandbox_author,
                             logger=logger)
        plenary = Plenary.get_plenary(dbhost, logger=logger)
        with plenary.get_key():
            dom.compile(session, only=plenary.object_templates,
                        panc_debug_include=pancinclude,
                        panc_debug_exclude=pancexclude,
                        cleandeps=cleandeps)
        return

    def render(self, session, logger, hostname,
               pancinclude, pancexclude, pancdebug, cleandeps, **_):
        template_domain, plenary = self._preprocess(session, logger, hostname)
        if pancdebug:
            pancinclude = r'.*'
            pancexclude = r'components/spma/functions.*'
        self._compile_template_domain(session, template_domain, plenary,
                                      pancinclude, pancexclude, cleandeps)

    @staticmethod
    def _preprocess(session, logger, hostname):
        dbhost = hostname_to_host(session, hostname)
        template_domain = TemplateDomain(dbhost.branch, dbhost.sandbox_author,
                                         logger=logger)
        plenary = Plenary.get_plenary(dbhost, logger=logger)
        return template_domain, plenary

    @staticmethod
    def _compile_template_domain(session, template_domain, plenary,
                                 pancinclude, pancexclude, cleandeps):
        with plenary.get_key():
            template_domain.compile(session, only=plenary.object_templates,
                                    panc_debug_include=pancinclude,
                                    panc_debug_exclude=pancexclude,
                                    cleandeps=cleandeps)
