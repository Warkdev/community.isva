# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import os

import pytest
from unittest.mock import MagicMock, patch

from ansible.module_utils.connection import Connection
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible_collections.community.isva.plugins.module_utils.isva_service_agreements import (
    fetch_service_agreements
)
from ansible_collections.community.isva.plugins.module_utils.common import ISVAModuleError

fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}

@pytest.fixture
def connection_mock():
    connection = Connection(socket_path='fake_socket')
    yield connection

@pytest.fixture
def accepted_agreements():
    yield {'code': 200, 'contents': {'configured': True}}

@pytest.fixture
def not_accepted_agreements():
    yield {'code': 200, 'contents': {'configured': False}}

@pytest.fixture
def unknown_code_response():
    yield {'code': 401, 'contents': {}}

class TestISVAServiceAgreements:
 
    def test_fetch_service_agreements_accepted_isva_1003(connection_mock, accepted_agreements):
        connection_mock.send_request = MagicMock()
        connection_mock.send_request.return_value = accepted_agreements
        assert fetch_service_agreements(connection_mock) == {'configured': True}

    def test_fetch_service_agreements_not_accepted_isva_1003(connection_mock, not_accepted_agreements):
        connection_mock.send_request = MagicMock()
        connection_mock.send_request.return_value = not_accepted_agreements
        assert fetch_service_agreements(connection_mock) == {'configured': False}

    def test_fetch_service_agreements_unknown_code(connection_mock, unknown_code_response):
        connection_mock.send_request = MagicMock()
        connection_mock.send_request.return_value = unknown_code_response
        with pytest.raises(ISVAModuleError):
            fetch_service_agreements(connection_mock)

