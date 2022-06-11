#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: isva_shared_volumes_import
short_description: Collect information about the service agreements status of the appliance
description:
  - Collect service agreements status from IBM ISVA devices.
version_added: "1.0.0"
author:
  - Cédric Servais (@7893254)
'''

EXAMPLES = r'''
- name: Accept ISVA Service Agreement
  isva_shared_volumes_import:
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

from ansible_collections.community.isva.plugins.module_utils.isva_shared_volumes import fetch_shared_volumes, upload_shared_volumes

from ansible_collections.community.isva.plugins.module_utils.isva_utils import (
    create_return_object, create_return_error, setup_logging, update_logging_info, convert_filesystem_to_dict
)

logger = logging.getLogger(__name__)
str_log = StringIO()
error_log = StringIO()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        file_spec = dict(
            name=dict(type='str', required=False),
            path=dict(type='str', required=True, choices=['fixpacks', 'snapshots', 'support']),
            src=dict(type='str', required=True),
            overwrite=dict(type='bool', default=False)
        )
        argument_spec = dict(
            files=dict(type='list', required=False, elements='dict', options=file_spec),
            path=dict(type='str', required=False, choices=['fixpacks', 'snapshots', 'support']),
            name=dict(type='str', required=False),
            src=dict(type='str', required=False),
            overwrite=dict(type='bool', default=False),
            log_level=dict(type='str', default='INFO', choices=['CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'])
        )
        self.argument_spec = {}
        self.argument_spec.update(argument_spec)
        self.required_one_of = [
            ['files', 'path'],
            ['files', 'src']
        ]
        self.mutually_exclusive = [
            ['files', 'path'],
            ['files', 'src']
        ]


def exec_module(module):
    check_mode = module.check_mode  # We donwload files also in checkmode.
    remote_files = convert_filesystem_to_dict(fetch_shared_volumes(module))
    files = module.params.get('files') or [{'path': module.params['path'], 'name': module.params['name'], 'src': module.params['src'], 'overwrite': module.params['overwrite']}]
    diff = {
        'before': [],
        'after': []
    }
    changed = False
    for f in files:
        path = f['path']
        volume = f['name']
        src = f['src']
        overwrite = f['overwrite']

        result = upload_shared_volumes(module, path, volume, src, overwrite, remote_files, check_mode)
        if result:
            diff['before'].append({'path': '{}/{}'.format(path, volume), 'state': 'absent'})
        else:
            diff['before'].append({'path': '{}/{}'.format(path, volume), 'state': 'file'})

        changed = changed or result

    return {'changed': changed}


def main():
    spec = ArgumentSpec()
    module = AnsibleModule(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode,
        mutually_exclusive=spec.mutually_exclusive,
        required_one_of=spec.required_one_of
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
        return_value = create_return_error(msg=str(e), stdout=str_log.getvalue(), stderr=error_log.getvalue())
        module.fail_json(**return_value)


if __name__ == '__main__':
    main()
