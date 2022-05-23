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

uri = '/isam/pending_changes'

logger = logging.getLogger(__name__)

def fetch_pending_changes(module):
    """ This function fetch the list of pending changes from the appliance.

    Returns:
        _type_: _description_
    """
    connection = Connection(module._socket_path)
    response = connection.send_request(path=uri)

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']

def count_pending_changes(module):
    """ This function fetch the number of pending changes from the appliance.

    Returns:
        _type_: _description_
    """
    connection = Connection(module._socket_path)
    response = connection.send_request(path='{}/count'.format(uri))

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']

def deploy_changes(module):
    """This function deploy the list of outsanding changes

    Args:
        module (_type_): _description_
    """
    connection = Connection(module._socket_path)
    response = connection.send_request(path=uri, method='PUT')

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']

def rollback_changes(module):
    """This function rollback the list of outsanding changes

    Args:
        module (_type_): _description_
    """
    connection = Connection(module._socket_path)
    response = connection.send_request(path=uri, method='DELETE')

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']