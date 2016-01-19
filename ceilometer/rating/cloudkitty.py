
# -*- coding: utf-8 -*-
#
# Copyright 2016 HopebayTech
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from keystoneclient import exceptions
from oslo_config import cfg
from oslo_log import log
from oslo_utils import timeutils
import six.moves.urllib.parse as urlparse
from cloudkittyclient import client as ck_client

from ceilometer.agent import plugin_base
from ceilometer import keystone_client
from ceilometer import sample

LOG = log.getLogger(__name__)

SERVICE_OPTS = [
    cfg.StrOpt('cloudkitty',
               default='rating',
               help='Cloudkitty service type.'),
]

cfg.CONF.register_opts(SERVICE_OPTS, group='service_types')


class _Base(plugin_base.PollsterBase):
    _ENDPOINT = None

    @property
    def default_discovery(self):
        return 'tenant'

    @staticmethod
    def _get_endpoint(ksclient):
        if _Base._ENDPOINT is None:
            try:
                conf = cfg.CONF.service_credentials
                ck_url = ksclient.service_catalog.url_for(
                    service_type=cfg.CONF.service_types.cloudkitty,
                    endpoint_type=conf.os_endpoint_type)
                _Base._ENDPOINT = urlparse.urljoin(ck_url, '')
            except exceptions.EndpointNotFound:
                LOG.debug("Cloudkitty endpoint not found")
        return _Base._ENDPOINT

    def _iter_accounts(self, ksclient, cache, tenants):
        return iter(list(self._get_account_info(ksclient, tenants)))

    def _get_account_info(self, ksclient, tenants):
        endpoint = self._get_endpoint(ksclient)
        if not endpoint:
            raise StopIteration()

        for t in tenants:
            cloudkitty = ck_client.Client('1', endpoint,
                                          token=ksclient.auth_token,
                                          insecure=True,
                                          cacert=None)

            yield(t.id, cloudkitty.reports.get_total(t.id))


class RatingCostPollster(_Base):
    """ Rating """

    def get_samples(self, manager, cache, resources):
        for tenant, cost in self._iter_accounts(manager.keystone,
                                                cache, resources):
            yield sample.Sample(
                name='cloudkitty.rating',
                type=sample.TYPE_CUMULATIVE,
                volume=int(float(cost)) if cost is not None else 0,
                unit='dollar',
                user_id=None,
                project_id=tenant,
                resource_id=tenant,
                timestamp=timeutils.utcnow().isoformat(),
                resource_metadata=None,
                )
