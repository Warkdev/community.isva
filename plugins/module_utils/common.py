# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import env_fallback
from ansible.module_utils.six import iteritems
from ansible.module_utils.parsing.convert_bool import (
    BOOLEANS_TRUE, BOOLEANS_FALSE
)
from collections import defaultdict

isva_provider_spec = {
    'server': dict(
        required=True,
        fallback=(env_fallback, ['ISVA_LMI_HOST'])
    ),
    'server_port': dict(
        type='int',
        default=443,
        fallback=(env_fallback, ['ISVA_LMI_PORT'])
    ),
    'user': dict(
        required=True,
        fallback=(env_fallback, ['ISVA_USER', 'ANSIBLE_NET_USERNAME'])
    ),
    'password': dict(
        required=True,
        no_log=True,
        aliases=['pass', 'pwd'],
        fallback=(env_fallback, ['ISVA_PASSWORD', 'ANSIBLE_NET_PASSWORD']),
    ),
    'validate_certs': dict(
        type='bool',
        default='yes',
        fallback=(env_fallback, ['ISVA_VALIDATE_CERTS'])
    ),
    'transport': dict(
        choices=['rest'],
        default='rest'
    ),
    'timeout': dict(type='int')
}

isva_argument_spec = {
    'provider': dict(type='dict', options=isva_provider_spec),
}

def get_provider_argspec():
    return isva_provider_spec

def load_params(params):
    provider = params.get('provider') or dict()
    for key, value in iteritems(provider):
        if key in isva_argument_spec:
            if params.get(key) is None and value is not None:
                params[key] = value

class AnsibleISVAParameters(object):
    def __init__(self, *args, **kwargs):
        self._values = defaultdict(lambda: None)
        self._values['__warnings'] = []
        self.provider = kwargs.pop('provider', None)
        self._module = kwargs.pop('module', None)
        self._params = {}

        params = kwargs.pop('params', None)
        if params:
            self.update(params=params)
            self._params.update(params)

    def update(self, params=None):
        if params:
            self._params.update(params)
            for k, v in iteritems(params):
                # Adding this here because ``username`` is a connection parameter
                # and in cases where it is also an API parameter, we run the risk
                # of overriding the specified parameter with the connection parameter.
                #
                # Since this is a problem, and since "username" is never a valid
                # parameter outside its usage in connection params (where we do not
                # use the ApiParameter or ModuleParameters classes) it is safe to
                # skip over it if it is provided.
                if k == 'password':
                    continue
                if self.api_map is not None and k in self.api_map:
                    map_key = self.api_map[k]
                else:
                    map_key = k

                # Handle weird API parameters like `dns.proxy.__iter__` by
                # using a map provided by the module developer
                class_attr = getattr(type(self), map_key, None)
                if isinstance(class_attr, property):
                    # There is a mapped value for the api_map key
                    if class_attr.fset is None:
                        # If the mapped value does not have
                        # an associated setter
                        self._values[map_key] = v
                    else:
                        # The mapped value has a setter
                        setattr(self, map_key, v)
                else:
                    # If the mapped value is not a @property
                    self._values[map_key] = v

    def api_params(self):
        result = {}
        for api_attribute in self.api_attributes:
            if self.api_map is not None and api_attribute in self.api_map:
                result[api_attribute] = getattr(self, self.api_map[api_attribute])
            else:
                result[api_attribute] = getattr(self, api_attribute)
        result = self._filter_params(result)
        return result

    def __getattr__(self, item):
        # Ensures that properties that weren't defined, and therefore stashed
        # in the `_values` dict, will be retrievable.
        return self._values[item]

    def _filter_params(self, params):
        return dict((k, v) for k, v in iteritems(params) if v is not None)

def flatten_boolean(value):
    truthy = list(BOOLEANS_TRUE) + ['enabled', 'True', 'true']
    falsey = list(BOOLEANS_FALSE) + ['disabled', 'False', 'false']
    if value is None:
        return None
    elif value in truthy:
        return 'yes'
    elif value in falsey:
        return 'no'

class Noop(object):
    pass

class ISVAModuleError(Exception):
    pass