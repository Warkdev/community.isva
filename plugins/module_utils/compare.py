# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re

from ansible.module_utils.six import iteritems

def cmp_simple_list(want, have):
    if want is None:
        return None
    if have is None and want in ['', 'none']:
        return None
    if have is not None and want in ['', 'none']:
        return []
    if have is None:
        return want
    if set(want) != set(have):
        return want
    return None


def cmp_str_with_none(want, have):
    if want is None:
        return None
    if have is None and want == '':
        return None
    if want != have:
        return want


def compare_complex_list(want, have):
    """Performs a complex list comparison

    A complex list is a list of dictionaries

    Args:
        want (list): List of dictionaries to compare with second parameter.
        have (list): List of dictionaries compare with first parameter.

    Returns:
        bool:
    """
    if want == [] and have is None:
        return None
    if want is None:
        return None
    w = []
    h = []
    for x in want:
        tmp = [(str(k), str(v)) for k, v in iteritems(x)]
        w += tmp
    for x in have:
        tmp = [(str(k), str(v)) for k, v in iteritems(x)]
        h += tmp
    if set(w) == set(h):
        return None
    else:
        return want


def compare_dictionary(want, have):
    """Performs a dictionary comparison

    Args:
        want (dict): Dictionary to compare with second parameter.
        have (dict): Dictionary to compare with first parameter.

    Returns:
        bool:
    """
    if want == {} and have is None:
        return None
    if want is None:
        return None
    w = [(str(k), str(v)) for k, v in iteritems(want)]
    h = [(str(k), str(v)) for k, v in iteritems(have)]
    if set(w) == set(h):
        return None
    else:
        return want

def version_compare(version1, version2):
    """
    Compare two ISAM version strings. Please note that the versions should be all numeric separated by dots.

    Returns following values:
         0 - if version strings are equivalent
        >0 - if version1 is greater than version2
        <0 - if version1 is less than version2

    Test cases to run for verifying this code:
        assert version_compare("1", "1") == 0
        assert version_compare("2.1", "2.2") < 0
        assert version_compare("3.0.4.10", "3.0.4.2") > 0
        assert version_compare("4.08", "4.08.01") < 0
        assert version_compare("3.2.1.9.8144", "3.2") > 0
        assert version_compare("3.2", "3.2.1.9.8144") < 0
        assert version_compare("1.2", "2.1") < 0
        assert version_compare("2.1", "1.2") > 0
        assert version_compare("5.6.7", "5.6.7") == 0
        assert version_compare("1.01.1", "1.1.1") == 0
        assert version_compare("1.1.1", "1.01.1") == 0
        assert version_compare("1", "1.0") == 0
        assert version_compare("1.0", "1") == 0
        assert version_compare("1.0", "1.0.1") < 0
        assert version_compare("1.0.1", "1.0") > 0
        assert version_compare("1.0.2.0", "1.0.2") == 0
        assert version_compare("10.0", "9.0.3") > 0

    :param version1:
    :param version2:
    :return:
    """

    def normalize(v):
        v = re.sub(r'_b\d+$', '', v)
        return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]

    if normalize(version1) == normalize(version2):
        return 0
    elif normalize(version1) > normalize(version2):
        return 1
    elif normalize(version1) < normalize(version2):
        return -1
