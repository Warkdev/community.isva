# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.community.isva.plugins.module_utils.isva_utils import parse_fail_message
from ansible_collections.community.isva.plugins.module_utils.common import ISVAModuleError
from ansible.module_utils.connection import Connection

import logging
import json

uri = '/isam/dsc/config'

logger = logging.getLogger(__name__)

MAP_API_ATTRIBUTES = {
    'worker_threads': 'worker_threads',
    'max_session_lifetime': 'max_session_lifetime',
    'client_grace': 'client_grace',
    'connection_idle_timeout': 'connection_idle_timeout',
    'service_port': 'service_port',
    'replication_port': 'replication_port',
    'servers': 'servers'
}

MAP_API_SERVER_ATTRIBUTES = {
    'ip': 'ip',
    'service_port': 'service_port',
    'replication_port': 'replication_port'
}


def from_module(source):
    data = {}
    for key in MAP_API_ATTRIBUTES:
        if key in source and source[key]:
            data[key] = source[key]

    return data


def from_api(source):
    data = {}
    for key, value in MAP_API_ATTRIBUTES.items():
        if value in source and source[value] is not None:
            data[key] = source[value]

    return data


def to_api(want):
    data = {}
    for key in MAP_API_ATTRIBUTES:
        if key in want:
            data[MAP_API_ATTRIBUTES[key]] = want[key]
    return data


def get_default():
    return {
        'servers': [],
        'worker_threads': 64,
        'replication_port': 444,
        'client_grace': 600,
        'max_session_lifetime': 3600,
        'connection_idle_timeout': 0,
        'service_port': 443
    }


def fetch_dsc_configuration(module):
    """ This function fetch the dsc configuration from the appliance.

    Returns:
        _type_: _description_
    """
    connection = Connection(module._socket_path)
    response = connection.send_request(path=uri)

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def update_dsc_configuration(module, payload):
    connection = Connection(module._socket_path)
    payload = json.dumps(payload)

    response = connection.send_request(path=uri, method='PUT', payload=payload)

    if response['code'] != 204:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']
