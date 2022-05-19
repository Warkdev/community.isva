# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import os

import mock

from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.module_utils.six import BytesIO, StringIO

from ansible_collections.community.internal_test_tools.tests.unit.compat import unittest
from ansible_collections.community.isva.plugins.httpapi.isva import HttpApi

fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}


def load_fixture(name):
    path = os.path.join(fixture_path, name)

    if path in fixture_data:
        return fixture_data[path]

    with open(path) as f:
        data = f.read()

    try:
        data = json.loads(data)
    except Exception:
        pass

    fixture_data[path] = data
    return data

class FakeISVAHttpApiPlugin(HttpApi):
    def __init__(self, conn):
        super(FakeISVAHttpApiPlugin, self).__init__(conn)
        self.hostvars = {}

    def get_option(self, var):
        return self.hostvars[var]

    def set_option(self, var, val):
        self.hostvars[var] = val

class TestISVAHttpapi(unittest.TestCase):
    def setUp(self):
        self.connection_mock = mock.Mock()
        self.isva_plugin = FakeISVAHttpApiPlugin(self.connection_mock)
        self.isva_plugin._load_name = 'httpapi'

    def test_send_request_should_return_error_info_when_http_error_raises(self):
        self.connection_mock.send.side_effect = HTTPError('http://testhost.com', 500, '', {},
                                                          StringIO('{"errorMessage": "ERROR"}'))

        resp = self.isva_plugin.send_request('/test', None)
        print(resp)

        assert resp == {'code': 500, 'contents': {'errorMessage': 'ERROR'}}

    '''
    def test_upload_file(self):
        self.connection.send.return_value = True
        binary_file = os.path.join(fixture_path, 'test_binary_file.mock')
        self.connection.httpapi.upload_file('/fake/path/to/upload', binary_file)

        self.connection.send.assert_called_once_with(
            '/fake/path/to/upload/test_binary_file.mock', ANY, method='POST',
            headers={'Content-Range': '0-307199/307200', 'Content-Type': 'application/octet-stream',
                     'Connection': 'keep-alive'
                     }
        )
    '''
    '''
    def test_upload_file_retry(self):
        self.connection.send.side_effect = [HTTPError(
            'http://bigip.local', 400, '', {}, StringIO('{"errorMessage": "ERROR"}')
        ), True]
        binary_file = os.path.join(fixture_path, 'test_binary_file.mock')
        self.connection.httpapi.upload_file('/fake/path/to/upload', binary_file)

        self.connection.send.assert_called_with(
            '/fake/path/to/upload/test_binary_file.mock', ANY, method='POST',
            headers={'Content-Range': '0-307199/307200', 'Content-Type': 'application/octet-stream',
                     'Connection': 'keep-alive'
                     }
        )
        assert self.connection.send.call_count == 2
    '''
    '''
    def test_upload_file_total_failure(self):
        self.connection.send.side_effect = HTTPError(
            'http://bigip.local', 400, '', {}, StringIO('{"errorMessage": "ERROR"}')
        )
        binary_file = os.path.join(fixture_path, 'test_binary_file.mock')

        with self.assertRaises(AnsibleConnectionFailure) as res:
            self.connection.httpapi.upload_file('/fake/path/to/upload', binary_file)

        assert 'Failed to upload file too many times.' in str(res.exception)
        assert self.connection.send.call_count == 3
    '''

    '''
    def test_download_file(self):
        self.connection.send.return_value = download_response('ab' * 50000)
        self.connection.download_file('/fake/path/to/download/fakefile', '/tmp/fakefile')
        self.connection.send.assert_called_with('/fake/path/to/download/fakefile', None,
                                                headers={'Content-Range': '0-99999/99999',
                                                         'Content-Type': 'application/octet-stream',
                                                         'Connection': 'keep-alive'}
                                                )
        assert os.stat('/tmp/fakefile').st_size == 100000
        # clean up
        os.remove('/tmp/fakefile')
    '''

    '''
    def test_download_file_http_error(self):
        self.connection.send.side_effect = [
            HTTPError('http://bigip.local', 400, '', {}, StringIO('{"errorMessage": "ERROR"}'))
        ]

        with self.assertRaises(HTTPError) as res:
            self.connection.download_file('/fake/path/to/download/fakefile', '/tmp/fakefile')

        assert res.exception.code == 400
    '''

    @staticmethod
    def _connection_response(response, status=200):
        response_mock = mock.Mock()
        response_mock.getcode.return_value = status
        response_text = json.dumps(response) if type(response) is dict else response
        response_data = BytesIO(response_text.encode() if response_text else ''.encode())
        return response_mock, response_data