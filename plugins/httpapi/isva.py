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
version_added: "1.0"
"""
import json

from ansible.module_utils.basic import to_text
from ansible.plugins.httpapi import HttpApiBase
from ansible.module_utils.six.moves.urllib.error import HTTPError

from ansible_collections.community.isva.plugins.module_utils.constants import (
    BASE_HEADERS
)

from ansible_collections.community.isva.plugins.module_utils.common import ISVAModuleError

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

    def send_request(self, path, method='GET', payload=None, headers=None):
        headers = headers if headers else BASE_HEADERS

        try:
            self._display_request(method, path, payload)
            response, response_data = self.connection.send(path, payload, method=method, headers=BASE_HEADERS)
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
