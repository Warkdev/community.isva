# -*- coding: utf-8 -*-
#
# Copyright: (c) 2020, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

BASE_HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json'}
BASE_DOWNLOAD_FILE_HEADERS = {'Accept': 'application/json,application/octet-stream', 'Connection': 'keep-alive'}
BASE_UPLOAD_FILE_HEADERS = {'Accept': 'application/json,text/html,application/xhtml+xml,application/xml'}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
