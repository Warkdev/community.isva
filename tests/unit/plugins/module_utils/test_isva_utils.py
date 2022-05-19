# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import os

import mock

from ansible_collections.community.internal_test_tools.tests.unit.compat import unittest
from ansible_collections.community.isva.plugins.module_utils.isva_utils import (
    parse_fail_message, create_return_object
)

fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}

