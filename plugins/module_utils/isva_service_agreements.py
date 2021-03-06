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

uri = '/setup_service_agreements/accepted'

logger = logging.getLogger(__name__)


def fetch_service_agreements(module):
    """ This function fetch the service agreements state from the appliance.

    Returns:
        _type_: _description_
    """
    connection = Connection(module._socket_path)
    response = connection.send_request(path=uri)

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def accept_service_agreements(module, **kwargs):
    connection = Connection(module._socket_path)
    accepted = kwargs.pop('accepted')
    payload = json.dump({'accepted': str(accepted)})

    response = connection.send_request(path=uri, method='PUT', payload=payload)

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']
