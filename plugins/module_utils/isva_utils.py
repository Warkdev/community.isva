# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import logging
import logging.config

logger = logging.getLogger(__name__)

def setup_logging(str_log, log_level):
    DEFAULT_LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(asctime)s] [PID:%(process)d TID:%(thread)d] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': log_level,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': str_log
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': log_level,
                'propagate': True
            }
        }
    }
    logging.config.dictConfig(DEFAULT_LOGGING)

def parse_fail_message(code, response):
    return 'ISVA device returned error {0} with message {1}'.format(code, response)

def update_logging_info(return_value, stdout='', stderr=''):
    return return_value.update({'stdout': stdout, 'stdout_lines': stdout.splitlines(), 'stderr': stderr, 'stderr_lines': stderr.splitlines()})

def create_return_error(msg='', stdout='', stderr=''):
    return {'msg': msg, 'stdout': stdout, 'stdout_lines': stdout.splitlines(), 'stderr': stderr, 'stderr_lines': stderr.splitlines()}

def create_return_object(changed=False, failed=False, rc=0, skipped=False, stderr='', stderr_lines=[], stdout='', stdout_lines=[]):
    return {'changed': changed, 'failed': failed, 'rc': rc, 'skipped': skipped, 'stderr': stderr, 'stderr_lines': stderr_lines, 'stdout': stdout, 'stdout_lines': stdout_lines}