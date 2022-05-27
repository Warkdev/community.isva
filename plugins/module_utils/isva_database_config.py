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

uri = '/isam/cluster/v2'

logger = logging.getLogger(__name__)

MAP_API_ATTRIBUTES = {
    'db_type': 'hvdb_db_type',
    'address': 'hvdb_address',
    'port': 'hvdb_port',
    'user': 'hvdb_user',
    'password': 'hvdb_password',
    'db_name': 'hvdb_db_name',
    'secure': 'hvdb_db_secure',
    'db2_alt_address': 'hvdb_db2_alt_address',
    'db2_alt_port': 'hvdb_db2_alt_port',
    'truststore': 'hvdb_db_truststore',
    'driver_type': 'hvdb_driver_type',
    'failover_servers': 'hvdb_failover_servers'
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
        if value in source and source[value]:
            data[key] = source[value]

    return data


def to_api(want):
    data = {}
    for key in MAP_API_ATTRIBUTES:
        if key in want:
            data[MAP_API_ATTRIBUTES[key]] = want[key]
    return data


def fetch_database_configuration(module):
    """ This function fetch the database configuration from the appliance.

    Returns:
        _type_: _description_
    """
    connection = Connection(module._socket_path)
    response = connection.send_request(path=uri)

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def update_database_configuration(module, payload):
    connection = Connection(module._socket_path)
    payload = json.dumps(payload)

    response = connection.send_request(path=uri, method='PUT', payload=payload)

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def create_database_configuration(module, payload):
    connection = Connection(module._socket_path)
    payload = json.dumps(payload)
    response = connection.send_request(path=uri, method='POST', payload=payload)

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']
