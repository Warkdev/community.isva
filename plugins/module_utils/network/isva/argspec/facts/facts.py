#
# -*- coding: utf-8 -*-
# Copyright 2022 Cédric Servais
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The arg spec for the isva facts module.
"""


class FactsArgs(object):  # pylint: disable=R0903
    """ The arg spec for the isva facts module
    """

    def __init__(self, **kwargs):
        pass

    choices = [
        'all',
        'service_agreements',
    ]

    argument_spec = {
        'gather_subset': dict(default=['!config'], type='list'),
        'gather_network_resources': dict(choices=choices,
                                         type='list'),
    }
