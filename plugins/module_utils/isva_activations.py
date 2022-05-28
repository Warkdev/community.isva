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

uri = '/isam/capabilities/{}v1'

logger = logging.getLogger(__name__)


def fetch_activation_offerings(module):
    """ This function fetch the system activation information from the appliance.

    Returns:
        _type_: _description_
    """
    connection = Connection(module._socket_path)
    response = connection.send_request(path=uri.format(''))

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def fetch_activation_offering(module, offering):
    """ This function fetch the system activation information from the appliance for the given offering.

    Returns:
        _type_: _description_
    """
    connection = Connection(module._socket_path)
    response = connection.send_request(path=uri.format('{}/'.format(offering)))

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def update_activation_offering(module, offering, payload):
    """ This function update the status of a given activation offering.

    Returns:
        _type_: _description_
    """
    connection = Connection(module._socket_path)
    payload = json.dumps(payload)
    response = connection.send_request(path=uri.format('{}/'.format(offering)), method='PUT', payload=payload)

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def create_activation_offering(module, payload):
    """ This function create the status of a given activation offering.

    Returns:
        _type_: _description_
    """
    connection = Connection(module._socket_path)
    payload = json.dumps(payload)
    response = connection.send_request(path=uri.format(''), method='POST', payload=payload)

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def delete_activation_offering(module, offering):
    """ This function deletes the activation offering.

    Returns:
        _type_: _description_
    """
    connection = Connection(module._socket_path)
    response = connection.send_request(path=uri.format('{}/'.format(offering)), method='DELETE')

    if response['code'] != 204:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']