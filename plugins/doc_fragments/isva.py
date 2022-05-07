# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):
    # Standard ISVA documentation fragment
    DOCUMENTATION = r'''
options:
  provider:
    description:
      - A dict object containing connection details.
    type: dict
    version_added: "1.0.0"
    suboptions:
      password:
        description:
          - The password for the user account used to connect to the ISVA.
          - You may omit this option by setting the environment variable C(ISVA_PASSWORD).
        type: str
        required: true
        aliases: [ pass, pwd ]
      server:
        description:
          - The ISVA LMI host.
          - You may omit this option by setting the environment variable C(ISVA_LMI_HOST).
        type: str
        required: true
      server_port:
        description:
          - The ISVA LMI port.
          - You may omit this option by setting the environment variable C(ISVA_LMI_PORT).
        type: int
        default: 443
      user:
        description:
          - The username to connect to the ISVA with. This user must have
            administrative privileges on the device.
          - You may omit this option by setting the environment variable C(ISVA_USER).
        type: str
        required: true
      validate_certs:
        description:
          - If C(no), SSL certificates are not validated. Use this only
            on personally controlled sites using self-signed certificates.
          - You may omit this option by setting the environment variable C(ISVA_VALIDATE_CERTS).
        type: bool
        default: yes
      timeout:
        description:
          - Specifies the timeout in seconds for communicating with the isva device
            for either connecting or sending commands.  If the timeout is
            exceeded before the operation is completed, the module will error.
        type: int
      transport:
        description:
          - Configures the transport connection to use when connecting to the
            remote device.
        type: str
        choices: [ rest ]
        default: rest
'''