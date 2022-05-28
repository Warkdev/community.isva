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

uri = '/isam/applang/v1'

logger = logging.getLogger(__name__)

MAP_API_ATTRIBUTES = {
    'application_locale': 'id'
}


def from_api(source):
    data = {}
    for _, value in MAP_API_ATTRIBUTES.items():
        if value in source and source[value] is not None:
            data = source[value]

    return data


def fetch_application_locale(module):
    """ This function fetch the application locale from the appliance

    Returns:
        _type_: _description_
    """
    connection = Connection(module._socket_path)
    response = connection.send_request(path=uri)

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']
