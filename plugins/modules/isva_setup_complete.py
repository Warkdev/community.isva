#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: isva_setup_complete
short_description: Collect information about the First Steps Setup process.
description:
  - Collect information about the First Steps Setup process.
version_added: "1.0.0"
author:
  - Cédric Servais (@7893254)
'''

EXAMPLES = r'''
- name: Accept ISVA First Steps status
  isva_setup_complete:
    configured: True
    state: replaced
'''

RETURN = r'''
gathered:
  description: A boolean indicating whether the service agreements have been accepted.
  returned: queried
  type: bool
  sample: true
'''

import logging
from io import StringIO

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.community.isva.plugins.module_utils.isva_setup_complete import fetch_first_steps, complete_first_steps

from ansible_collections.community.isva.plugins.module_utils.isva_utils import (
    create_return_object, create_return_error, setup_logging, update_logging_info
)

logger = logging.getLogger(__name__)
str_log = StringIO()
error_log = StringIO()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(
            state=dict(type='str', required=True, choices=['replaced']),
            configured=dict(type='bool', required=True, choices=[True]),
            log_level=dict(type='str', default='INFO', choices=['CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'])
        )
        self.argument_spec = {}
        self.argument_spec.update(argument_spec)


def __exec_replaced(module, **kwargs):
    check_mode = module.check_mode
    configured = module.params['configured']
    if kwargs.pop('configured') != configured:
        logger.debug('Completing First steps setup')
        if check_mode:
            return {'changed': True, 'after': {'configured': True}}

        complete_first_steps(module=module)
        return {'changed': True, 'after': {'configured': True}}

    return {'changed': False, 'after': {'configured': True}}


def exec_module(module):
    state = module.params['state']

    if state == 'replaced':
        before = fetch_first_steps(module=module)
        response = __exec_replaced(module=module, **before)
        return {'changed': response['changed'], 'diff': {'before': before, 'after': response['after']}}

    return {}


def main():
    spec = ArgumentSpec()
    module = AnsibleModule(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode
    )
    try:
        setup_logging(str_log, module._verbosity)
        logger.debug('Module parameters {}'.format(module.params))

        response = exec_module(module)
        return_value = create_return_object()
        update_logging_info(return_value, str_log.getvalue(), error_log.getvalue())
        return_value.update(response)

        module.exit_json(**return_value)
    except Exception as e:
        error_log.write(str(e))
        error_log.write(str(e.code))
        return_value = create_return_error(msg=str(e), stdout=str_log.getvalue(), stderr=error_log.getvalue())
        module.fail_json(**return_value)


if __name__ == '__main__':
    main()
