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

uri = '/adv_params'

logger = logging.getLogger(__name__)

MAP_API_ATTRIBUTES = {
    'advanced_tuning_parameters': 'tuningParameters'
}


def from_api(source):
    data = {}
    for _, value in MAP_API_ATTRIBUTES.items():
        if value in source and source[value] is not None:
            for param in source[value]:
                data[param['key']] = {'value': param['value'], 'comment': param['comment']}

    return data

def fetch_advanced_tuning_parameters(module):
    """ This function fetch the advanced tuning parameters from the appliance

    Returns:
        _type_: _description_
    """
    connection = Connection(module._socket_path)
    response = connection.send_request(path=uri)

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']
