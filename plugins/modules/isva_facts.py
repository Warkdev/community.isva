#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: isva_facts
short_description: Collect information from IBM ISVA devices
description:
  - Collect information from IBM ISVA devices.
version_added: "1.0.0"
extends_documentation_fragment: community.isva.modules.isva
author:
  - Cédric Servais (@7893254)
'''

EXAMPLES = r'''
- name: Collect ISVA information:
  isva_facts:
    provider:
      server: isva.mydomain.com
      user: admin
      password: secret
  delegate_to: localhost
'''

RETURN = r'''
product_name:
  description: The short product name
  returned: queried
  type: str
  sample: isva
product_description:
  description: The full product name
  returned: queried
  type: str
  sample: IBM Security Verify Access
firware_version:
  description: The firmware version, in the format "X.X.X.X"
  returned: queried
  type: str
  sample: 10.0.0.0
firmware_build:
  description: The firmware build label, in the format "YYYYMMDD-HHMM"
  returned: queried
  type: str
  sample: 20200612-0420
firmware_label:
  description: The full firmware build label
  returned: queried
  type: str
  sample: isva_10.0.0.0_20200612-0420
deployment_model:
  description: The deployment model. The possible values are C(Appliance) and C(Docker)
  returned: queried
  type: str
  sample: Appliance
'''

from ..module_utils.common import AnsibleISVAParameters, ISVAModuleError, flatten_boolean, isva_argument_spec
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import Request, ConnectionError
from ansible.module_utils.six import (
    iteritems, string_types
)

try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        self.argument_spec = {}
        self.argument_spec.update(isva_argument_spec)

class BaseManager(object):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.provider = kwargs.get('provider', None)
        self.kwargs = kwargs

    def exec_module(self):
        #start = datetime.datetime.now().isoformat()
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        return results

class Parameters(AnsibleISVAParameters):
    @property
    def gather_subset(self):
        if isinstance(self._values['gather_subset'], string_types):
            self._values['gather_subset'] = [self._values['gather_subset']]
        elif not isinstance(self._values['gather_subset'], list):
            raise ISVAModuleError(
                "The specified gather_subset must be a list."
            )
        tmp = list(set(self._values['gather_subset']))
        tmp.sort()
        self._values['gather_subset'] = tmp

        return self._values['gather_subset']

class BaseParameters(Parameters):
    @property
    def enabled(self):
        return flatten_boolean(self._values['enabled'])

    @property
    def disabled(self):
        return flatten_boolean(self._values['disabled'])

    def _remove_internal_keywords(self, resource):
        pass

    def to_return(self):
        result = {}
        for returnable in self.returnables:
            result[returnable] = getattr(self, returnable)
        result = self._filter_params(result)
        return result

class VersionFactParameters(BaseParameters):
    api_map = {
    }

    returnables = [
        'product_name',
        'product_description',
        'firmware_version',
        'firmware_build',
        'firmware_label',
        'deployment_model'
    ]

class VersionFactManager(BaseManager):
    def __init__(self, *args, **kwargs):
        self.provider = kwargs.get('provider', None)
        self.module = kwargs.get('module', None)
        super(VersionFactManager, self).__init__(**kwargs)

    def exec_module(self):
        facts = self._exec_module()
        result = dict(apm_access_profiles=facts)
        return result

    def _exec_module(self):
        results = []
        facts = self.read_facts()
        for item in facts:
            attrs = item.to_return()
            results.append(attrs)
        results = sorted(results, key=lambda k: k['full_path'])
        return results

    def read_facts(self):
        results = []
        collection = self.read_collection_from_device()
        for resource in collection:
            params = VersionFactParameters(params=resource)
            results.append(params)
        return results

    def read_collection_from_device(self):
        uri = "https://{0}:{1}/core/sys/versions".format(
            self.provider['server'],
            self.provider['server_port'],
        )
        resp = Request.get(uri)
        try:
            response = resp.json()
        except ValueError as ex:
            raise ISVAModuleError(str(ex))

        if resp.status not in [200, 201] or 'code' in response and response['code'] not in [200, 201]:
            raise ISVAModuleError(resp.content)

        if 'items' not in response:
            return []
        result = response['items']
        return result

class ModuleManager(object):
    def __init__(self, *args, **kwargs):
        self.module = kwargs.get('module', None)
        self.provider = kwargs.get('provider', None)
        self.kwargs = kwargs
        self.want = self.module.params
        self.managers = {
            'version': dict(
                manager=VersionFactManager,
                provider=self.provider,
            )
        }

    def exec_module(self):
        self.handle_all_keyword()
        result = self.filter_excluded_facts()

        managers = []
        for name in result:
            manager = self.get_manager(name)
            if manager:
                managers.append(manager)

        if not managers:
            result = dict(
                changed=False
            )
            return result

        result = self.execute_managers(managers)
        if result:
            result['changed'] = True
        else:
            result['changed'] = False
        return result

    def filter_excluded_facts(self):
        # Remove the excluded entries from the list of possible facts
        exclude = [x[1:] for x in self.want.gather_subset if x[0] == '!']
        include = [x for x in self.want.gather_subset if x[0] != '!']
        result = [x for x in include if x not in exclude]
        return result

    def handle_all_keyword(self):
        if 'all' not in self.want.gather_subset:
            return
        managers = list(self.managers.keys()) + self.want.gather_subset
        managers.remove('all')
        self.want.update({'gather_subset': managers})

    def execute_managers(self, managers):
        results = dict()
        for manager in managers:
            result = manager.exec_module()
            results.update(result)
        return results

    def get_manager(self, which):
        result = {}
        info = self.managers.get(which, None)
        if not info:
            return result
        kwargs = dict()
        kwargs.update(self.kwargs)

        manager = info.get('manager', None)
        provider = info.get('provider', None)
        kwargs['provider'] = provider(**self.module.params)
        result = manager(**kwargs)
        return result

def main():
  spec = ArgumentSpec()
  module = AnsibleModule(
    argument_spec=spec.argument_spec,
    supports_check_mode=spec.supports_check_mode
  )
  try:
    mm = ModuleManager(module=module)
    results = mm.exec_module()
    
    ansible_facts = dict()

    for key, value in iteritems(results):
        key = 'ansible_net_%s' % key
        ansible_facts[key] = value

    module.exit_json(ansible_facts=ansible_facts, **results)
  except Exception as e:
    module.fail_json(msg=str(ex))

if __name__ == '__main__':
  main()