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
import os

uri = '/shared_volume'
ALLOWED_PATH = ['fixpacks', 'snapshots', 'support']

logger = logging.getLogger(__name__)

MAP_API_ATTRIBUTES = {}


def from_api(source):
    data = {}
    for _, value in MAP_API_ATTRIBUTES.items():
        if value in source and source[value] is not None:
            data = source[value]

    return data


def _check_path(path):
    if path not in ALLOWED_PATH:
        raise ISVAModuleError('Invalid path {} provided, expected one of {}'.format(path, ALLOWED_PATH))


def fetch_shared_volumes(module, path=None, recursive=True):
    """ This function fetch the shared volumes from the appliance for a given path

    Returns:
        _type_: _description_
    """
    if path:
        _check_path(path)
        target_uri = '{}/{}?recursive={}'.format(uri, path, recursive)
    else:
        target_uri = '{}?recursive={}'.format(uri, recursive)

    connection = Connection(module._socket_path)
    response = connection.send_request(path=target_uri)

    if response['code'] != 200:
        raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def download_shared_volumes(module, path, volume, dest, remote_files={}):
    """This function will download the requested shared volume file.

    """
    _check_path(path)
    target_uri = '{}/{}/{}?type=File&export'.format(uri, path, volume)

    if path in remote_files and volume not in remote_files[path]:
        raise ISVAModuleError('The requested file does not exist {}/{}'.format(path, volume))

    want = remote_files[path][volume]['sha256']

    if os.path.isfile(dest):
        have = module.sha256(dest)
        if want == have:  # Don't download file if we already have it.
            return False

    connection = Connection(module._socket_path)
    # Need to pass-in empty headers or the appliance responds with a JSON.
    response = connection.download_file(path=target_uri, dest=dest, headers={})

    if not response:
        raise ISVAModuleError('Couldn\'t download the file {}/{}'.format(volume, path))

    have = module.sha256(dest)
    if want != have:  # Throw error if downloaded file doesn't have the same checksum as remote
        raise ISVAModuleError('The downloaded file checksum doesn\'t match the remote one: {} - {}'.format(want, have))

    return True


def upload_shared_volumes(module, path, volume, src, overwrite=False):
    """This function will upload the requested shared volume file.
    """
    _check_path(path)

    if not os.path.isfile(src):
        raise ISVAModuleError('The source file is not valid {}'.format(src))

    with open(src, 'rb') as f:
        data = {
            'file': f.read(),
            'force': overwrite
        }

        target_uri = '{}/{}/{}'.format(uri, path, volume)

        connection = Connection(module._socket_path)
        response = connection.send_request(path=target_uri, method='POST', data=data)

        if response['code'] != 200:
            raise ISVAModuleError(parse_fail_message(response['code'], response['contents']))

        return response['contents']