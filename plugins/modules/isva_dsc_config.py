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
module: isva_dsc_config
short_description: Collect information about the First Steps Setup process.
description:
  - Collect information about the First Steps Setup process.
version_added: "1.0.0"
author:
  - Cédric Servais (@7893254)
'''

EXAMPLES = r'''
- name: Collect ISVA First Steps status
  isva_dsc_config:
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

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import recursive_diff

from ansible_collections.community.isva.plugins.module_utils.isva_dsc_config import (
    to_api, from_api, from_module, fetch_dsc_configuration, update_dsc_configuration, get_default
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
        server_spec = dict(
            ip=dict(type='str', required=True),
            service_port=dict(type='int', required=True),
            replication_port=dict(type='int', required=True)
        )
        dsc_spec = dict(
            worker_threads=dict(type='int', required=True),
            max_session_lifetime=dict(type='int', required=True),
            client_grace=dict(type='int', required=True),
            connection_idle_timeout=dict(type='int', required=True),
            service_port=dict(type='int', required=True),
            replication_port=dict(type='int', required=True),
            servers = dict(type='list', elements='dict', options=server_spec)
        )
        argument_spec = dict(
            state=dict(type='str', required=True, choices=['gathered', 'replaced', 'deleted']),
            dsc=dict(type='dict', required=False, options=dsc_spec)
        )
        self.argument_spec = {}
        self.argument_spec.update(argument_spec)
        self.required_if = [
            ['state', 'replaced', ['dsc'], True]
        ]


def __exec_gathered(module):
    response = fetch_dsc_configuration(module=module)
    data = from_api(response)
    return data


def __exec_replaced(module, **kwargs):
    check_mode = module.check_mode
    have = kwargs
    want = from_module(module.params['dsc'])

    diff = recursive_diff(have, want)
    if diff:  # Execute only if there were changes
        payload = to_api(want)

        if check_mode:
            return {'changed': True, 'diff': {'before': diff[0], 'after': diff[1]}}

        response = update_dsc_configuration(module=module, payload=payload)
        if 'warning' in response:
            return {'changed': True, 'diff': {'before': diff[0], 'after': diff[1]}, 'warnings': [response['warning']]}
        return {'changed': True, 'diff': {'before': diff[0], 'after': diff[1]}}

    return {'changed': False}

def __exec_deleted(module, **kwargs):
    check_mode = module.check_mode
    have = kwargs
    want = get_default()

    diff = recursive_diff(have, want)
    if diff:  # Execute only if there were changes
        payload = to_api(want)

        if check_mode:
            return {'changed': True, 'diff': {'before': diff[0], 'after': diff[1]}}

        response = update_dsc_configuration(module=module, payload=payload)
        if 'warning' in response:
            return {'changed': True, 'diff': {'before': diff[0], 'after': diff[1]}, 'warnings': [response['warning']]}
        return {'changed': True, 'diff': {'before': diff[0], 'after': diff[1]}}

    return {'changed': False}

def exec_module(module):
    state = module.params['state']

    if state == 'gathered':
        response = __exec_gathered(module=module)
        return {'gathered': response}
    elif state == 'replaced':
        before = __exec_gathered(module=module)
        response = __exec_replaced(module=module, **before)
        return response
    elif state == 'deleted':
        before = __exec_gathered(module=module)
        response = __exec_deleted(module=module, **before)
        return response

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
