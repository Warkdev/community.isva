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

uri = '/lmi'

logger = logging.getLogger(__name__)

MAP_API_ATTRIBUTES = {
    'start_time': 'start_time'
}


def from_api(source):
    data = {}
    source = source[0]  # Don't ask why IBM decided to put a dict into a single-item array.
    for key, value in MAP_API_ATTRIBUTES.items():
        if value in source and source[value] is not None:
            data[key] = source[value]

    return data


def fetch_lmi_status(module):
    """ This function fetch the lmi status from the appliance

    Returns:
        _type_: _description_
    """
    connection = Connection(module._socket_path)
    response = connection.send_request(path=uri)

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']
