#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: isva_service_agreements_info
short_description: Collect information about the service agreements status of the appliance
description:
  - Collect service agreements status from IBM ISVA devices.
version_added: "1.0.0"
extends_documentation_fragment: community.isva.modules.isva
author:
  - Cédric Servais (@7893254)
'''

EXAMPLES = r'''
- name: Collect ISVA Service Agreement information:
  isva_service_agreements_info:
  delegate_to: localhost
'''

RETURN = r'''
service_agreements_accepted:
  description: A boolean indicating whether the service agreements have been accepted.
  returned: queried
  type: bool
  sample: true
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection

from ansible_collections.community.isva.plugins.module_utils.isva_service_agreements import fetch_service_agreements

from ansible_collections.community.isva.plugins.module_utils.isva_utils import (
    create_return_object
)

MAPPED_ARGUMENTS = {'accepted': 'service_agreements_accepted'}

class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = {}
        self.argument_spec = {}
        self.argument_spec.update(argument_spec)

def exec_module(module, connection):
    response = fetch_service_agreements(connection=connection)
    return response

def main():
    spec = ArgumentSpec()
    module = AnsibleModule(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode
    )
    try:
        connection = Connection(module._socket_path)
        response = exec_module(module, connection)
        return_value = create_return_object()
        for mapper in MAPPED_ARGUMENTS:
          if mapper in response:
            response[MAPPED_ARGUMENTS[mapper]] = response[mapper]
            del response[mapper]
            
        return_value.update(response)

        module.exit_json(**return_value)
    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()