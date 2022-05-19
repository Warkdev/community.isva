# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
author: Cédric Servais <cedric.servais@outlook.com>
httpapi: isva
short_description: HttpApi Plugin for IBM ISVA devices
description:
  - This HttpApi plugin provides methods to connect to ISVA
    devices over a HTTP(S)-based api.
options:
  bigip_provider:
    description:
    - The login provider used in communicating with BIG-IP devices when the API connection
      is first established.
    - If the provider is not specified, the default C(tmos) value is assumed.
    ini:
    - section: defaults
      key: f5_provider
    env:
    - name: F5_PROVIDER
    vars:
    - name: f5_provider
version_added: "1.0"
"""
import os

from tempfile import NamedTemporaryFile

from ansible.module_utils.basic import to_text
from ansible.plugins.httpapi import HttpApiBase
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.errors import AnsibleConnectionFailure

from ansible_collections.community.isva.plugins.module_utils.constants import (
    BASE_HEADERS
)

from ansible_collections.community.isva.plugins.module_utils.common import ISVAModuleError


try:
    import json
except ImportError:
    import simplejson as json


class HttpApi(HttpApiBase):
    def __init__(self, connection):
        super(HttpApi, self).__init__(connection)
        self.connection = connection
        self.user = None

    def handle_httperror(self, exc):
        if exc.code == 404:
            # 404 errors need to be handled upstream due to exists methods relying on it.
            # Other codes will be raised by underlying connection plugin.
            return exc
        if exc.code == 401:
            if self.connection._auth is not None:
                # only attempt to refresh token if we were connected before not when we get 401 on first attempt
                self.connection._auth = None
                return True
        return False

    def send_request(self, url, method=None, **kwargs):
        body = kwargs.pop('data', None)
        # allow for empty json to be passed as payload, useful for some endpoints
        data = json.dumps(body) if body or body == {} else None
        try:
            self._display_request(method, url, body)
            response, response_data = self.connection.send(url, data, method=method, headers=BASE_HEADERS, **kwargs)
            response_value = self._get_response_value(response_data)
            return dict(
                code=response.getcode(),
                contents=self._response_to_json(response_value)
            )
        except HTTPError as e:
            return dict(code=e.code, contents=json.loads(e.read()))

    def _display_request(self, method, url, data=None):
        if data:
            self._display_message(
                'ISVA API Call: {0} to {1} with data {2}'.format(method, url, data)
            )
        else:
            self._display_message(
                'ISVA API Call: {0} to {1}'.format(method, url)
            )

    def _display_message(self, msg):
        self.connection._log_messages(msg)

    def _get_response_value(self, response_data):
        return to_text(response_data.getvalue())

    def _response_to_json(self, response_text):
        try:
            return json.loads(response_text) if response_text else {}
        # JSONDecodeError only available on Python 3.5+
        except ValueError:
            raise ISVAModuleError('Invalid JSON response: %s' % response_text)

    def network_os(self):
        return self.connection._network_os
