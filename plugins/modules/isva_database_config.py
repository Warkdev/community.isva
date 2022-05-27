#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

from requests import JSONDecodeError

__metaclass__ = type

DOCUMENTATION = r'''
---
module: isva_database_config
short_description: Collect information about the First Steps Setup process.
description:
  - Collect information about the First Steps Setup process.
version_added: "1.0.0"
author:
  - Cédric Servais (@7893254)
'''

EXAMPLES = r'''
- name: Collect ISVA First Steps status
  isva_database_config:
    state: gathered
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
import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import recursive_diff

from ansible_collections.community.isva.plugins.module_utils.isva_database_config import (
    to_api, from_api, from_module,
    create_database_configuration, fetch_database_configuration
)

from ansible_collections.community.isva.plugins.module_utils.isva_utils import (
    create_return_object, create_return_error, setup_logging, update_logging_info
)

logger = logging.getLogger(__name__)
str_log = StringIO()
error_log = StringIO()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        failover_spec = dict(
            address=dict(type='str', required=True),
            port=dict(type='int', required=True),
            order=dict(type='int', required=True)
        )
        hvdb_spec = dict(
            db_type=dict(type='str', required=True, choices=['db2', 'postgresql', 'oracle']),
            address=dict(type='str', required=True),
            port=dict(type='int', required=True),
            user=dict(type='str', required=True),
            password=dict(type='str', required=False, no_log=True),
            db_name=dict(type='str', required=True),
            secure=dict(type='bool', required=True, choices=[True, False]),
            # DB2 specific
            db2_alt_address=dict(type='str', required=False),
            db2_alt_port=dict(type='int', required=False),
            # Oracle specific
            truststore=dict(type='str', required=False),
            driver_type=dict(type='str', required=False),
            # Postgresql specific
            failover_servers=dict(type='list', elements='dict', options=failover_spec, required=False)
        )
        argument_spec = dict(
            state=dict(type='str', required=True, choices=['gathered', 'replaced']),
            hvdb=dict(type='dict', required=False, options=hvdb_spec)
        )
        self.argument_spec = {}
        self.argument_spec.update(argument_spec)
        self.required_if = [
            ['state', 'replaced', ['hvdb'], True]
        ]


def __exec_gathered(module):
    response = fetch_database_configuration(module=module)
    data = from_api(response)
    return data


def __exec_replaced(module, **kwargs):
    check_mode = module.check_mode
    logger.info(kwargs)
    have = kwargs
    want = from_module(module.params['hvdb'])

    if recursive_diff(have, want):  # Execute only if there were changes
        payload = to_api(want)

        if check_mode:
            return {'changed': True, 'after': want}

        response = create_database_configuration(module=module, payload=payload)
        if 'warning' in response:
            return {'changed': True, 'after': want, 'warnings': [response['warning']]}
        return {'changed': True, 'after': want}

    return {'changed': False, 'after': want}


def exec_module(module):
    state = module.params['state']

    if state == 'gathered':
        response = __exec_gathered(module=module)
        return {'gathered': response}
    elif state == 'replaced':
        before = __exec_gathered(module=module)
        response = __exec_replaced(module=module, **before)
        return {'changed': response['changed'], 'diff': {'before': before, 'after': response['after']}, 'warnings': response.get('warnings', [])}

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
        if 'code' in e:
            error_log.write(str(e.code))
        return_value = create_return_error(msg=str(e), stdout=str_log.getvalue(), stderr=error_log.getvalue())
        module.fail_json(**return_value)


if __name__ == '__main__':
    main()
