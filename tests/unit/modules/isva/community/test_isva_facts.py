# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import pytest
import sys

if sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip("F5 Ansible modules require Python >= 2.7")

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import iteritems

from plugins.modules.isva_facts import (
    Parameters, VersionFactManager, ArgumentSpec, ModuleManager
)
from tests.unit.compat import unittest
from tests.unit.compat.mock import Mock, patch
from tests.unit.modules.utils import set_module_args


fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}
