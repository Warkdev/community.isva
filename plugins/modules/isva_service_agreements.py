#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: isva_service_agreements
short_description: Collect information about the service agreements status of the appliance
description:
  - Collect service agreements status from IBM ISVA devices.
version_added: "1.0.0"
author:
  - Cédric Servais (@7893254)
'''

EXAMPLES = r'''
- name: Collect ISVA Service Agreement information
  isva_service_agreements:
    state: gathered

- name: Accept ISVA Service Agreement
  isva_service_agreements:
    accepted: True
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

from ansible_collections.community.isva.plugins.module_utils.isva_service_agreements import accept_service_agreements, fetch_service_agreements

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
            state=dict(type='str', required=True, choices=['replaced', 'gathered']),
            accepted=dict(type='bool', choices=[True]),
            log_level=dict(type='str', default='INFO', choices=['CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'])
        )
        self.argument_spec = {}
        self.argument_spec.update(argument_spec)
        self.required_if = [
            ['state', 'replaced', ['accepted'], True]
        ]


def __exec_gathered(module):
    response = fetch_service_agreements(module=module)
    return response


def __exec_replaced(module, **kwargs):
    check_mode = module.check_mode
    accepted = module.params['accepted']
    if kwargs.pop('accepted') != accepted:
        logger.debug('Updating service agreements')
        if check_mode:
            return {'changed': True, 'after': {'accepted': True}}

        response = accept_service_agreements(accepted=accepted)
        return {'changed': True, 'after': response}

    return {'changed': False, 'after': {'accepted': True}}


def exec_module(module):
    state = module.params['state']

    if state == 'gathered':
        response = __exec_gathered(module=module)
        return {'gathered': response}
    elif state == 'replaced':
        before = fetch_service_agreements(module=module)
        response = __exec_replaced(module=module, **before)
        return {'changed': response['changed'], 'diff': {'before': before, 'after': response['after']}}

    return {}


def main():
    spec = ArgumentSpec()
    module = AnsibleModule(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode,
        required_if=spec.required_if
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
