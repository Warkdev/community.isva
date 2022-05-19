# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

def parse_fail_message(code, response):
    return 'ISVA device returned error {0} with message {1}'.format(code, response)

def create_return_object(changed=False, failed=False, rc=0, skipped=False, stderr='', stderr_lines=[], stdout='', stdout_lines=[]):
    return {'changed': changed, 'failed': failed, 'rc': rc, 'skipped': skipped, 'stderr': stderr, 'stderr_lines': stderr_lines, 'stdout': stdout, 'stdout_lines': stdout_lines}