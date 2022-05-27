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

uri = '/docker/publish'

logger = logging.getLogger(__name__)


def publish_configuration(module):
    """ This function publish the current configuration to the shared volume.

    Returns:
        _type_: _description_
    """
    connection = Connection(module._socket_path)
    response = connection.send_request(path=uri, method='PUT')

    if response['code'] != 201:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']
