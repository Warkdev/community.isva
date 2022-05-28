# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.community.isva.plugins.module_utils.isva_utils import parse_fail_message
from ansible_collections.community.isva.plugins.module_utils.common import ISVAModuleError
from ansible.module_utils.connection import Connection

import json
import logging

uri = '/admin_cfg'

logger = logging.getLogger(__name__)

MAP_API_ATTRIBUTES = {
    ('heap_size', 'min'): 'minHeapSize',
    ('heap_size', 'max'): 'maxHeapSize',
    ('session', 'timeout'): 'sessionTimeout',
    ('session', 'inactive_timeout'): 'sessionInactiveTimeout',
    ('session', 'cache_purge'): 'sessionCachePurge',
    ('session', 'ba_timeout'): 'baSessionTimeout',
    'http_port': 'httpPort',
    'https_port': 'httpsPort',
    'sshd_client_alive_interval': 'sshdClientAliveInterval',
    'swap_file_size': 'swapFileSize',
    ('threads', 'min'): 'minThreads',
    ('threads', 'max'): 'maxThreads',
    'max_pool_size': 'maxPoolSize',
    'lmi_debug': 'lmiDebuggingEnabled',
    'console_log_level': 'consoleLogLevel',
    ('client_certs', 'accept'): 'acceptClientCerts',
    ('client_certs', 'validate_identity'): 'validateClientCertIdentity',
    ('client_certs', 'exclude_csrf_pattern'): 'excludeCsrfChecking',
    ('tls', 'server_protocol'): 'enabledServerProtocols',
    ('tls', 'enabled_protocol'): 'enabledTLS',
    ('files', 'max'): 'maxFiles',
    ('files', 'max_size'): 'maxFileSize',
    ('proxy', 'http'): 'httpProxy',
    ('proxy', 'https'): 'httpsProxy',
    ('login', 'header'): 'loginHeader',
    ('login', 'message'): 'loginMessage',
    'access_log_format': 'accessLogFormat',
    'lmi_message_timeout': 'lmiMessageTimeout',
    'valid_verify_domains': 'validVerifyDomains'
}


def from_api(source):
    data = {}
    for key, value in MAP_API_ATTRIBUTES.items():
        if value in source and source[value] is not None:
            if isinstance(key, tuple):
                if key[0] not in data:
                    data[key[0]] = {}
                data[key[0]][key[1]] = source[value]
            elif isinstance(key, str):
                data[key] = source[value]
        else:
            if isinstance(key, tuple):
                if key[0] not in data:
                    data[key[0]] = {}
                data[key[0]][key[1]] = None
            elif isinstance(key, str):
                data[key] = None

    return data

def fetch_administrator_settings(module):
    """ This function fetch the administrator settings information from the appliance

    Returns:
        _type_: _description_
    """
    connection = Connection(module._socket_path)
    response = connection.send_request(path=uri)

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']
