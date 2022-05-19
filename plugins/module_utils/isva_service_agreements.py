# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.community.isva.plugins.module_utils.isva_utils import parse_fail_message
from ansible_collections.community.isva.plugins.module_utils.common import ISVAModuleError

uri = '/setup_service_agreements/accepted'

def fetch_service_agreements(connection):
    """ This function fetch the service agreements state from the appliance.

    Args:
        connection (Connection): _description_

    Returns:
        _type_: _description_
    """
    response = connection.send_request(url=uri)

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']
