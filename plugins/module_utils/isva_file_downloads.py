# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.community.isva.plugins.module_utils.isva_utils import parse_fail_message, identical_files
from ansible_collections.community.isva.plugins.module_utils.common import ISVAModuleError
from ansible.module_utils.connection import Connection

import json
import logging
import os
import base64
import shutil

uri = '/isam/downloads'

logger = logging.getLogger(__name__)

MAP_API_ATTRIBUTES = {}


def from_api(source):
    data = {}
    for _, value in MAP_API_ATTRIBUTES.items():
        if value in source and source[value] is not None:
            data = source[value]

    return data


def fetch_file_downloads(module, path=None, recursive=True):
    """ This function fetch the file downloads from the appliance for a given path

    Returns:
        _type_: _description_
    """
    if path:
        target_uri = '{}/{}?recursive={}'.format(uri, path, recursive)
    else:
        target_uri = '{}?recursive={}'.format(uri, recursive)

    connection = Connection(module._socket_path)
    response = connection.send_request(path=target_uri)

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def download_file_downloads(module, path, dest, remote_files={}):
    """This function will download the requested shared volume file.

    """
    target_uri = '{}/{}'.format(uri, path)
    file_path = path.split('/')

    curr_d = remote_files
    for d in file_path[1:]:  # Starting at 1 to avoid the first empty string
        curr_d = curr_d.get(d)
        if not curr_d:
            raise ISVAModuleError('The requested file does not exist {}'.format(path))

    tmp_dest = '{}{}'.format(module.tmpdir, file_path[-1])
    # Downloading file, we've no way to find out remotely if they are identical, so adding it at a temporary location.
    connection = Connection(module._socket_path)
    response = connection.download_file(path=target_uri, dest=tmp_dest)

    if not response:
        raise ISVAModuleError('Couldn\'t download the file {}/{}'.format(volume, path))

    if identical_files(module, tmp_dest, dest):  # No change to report
        return False

    shutil.copyfile(tmp_dest, dest)

    return True
