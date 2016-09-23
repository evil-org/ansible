# Make coding more python3-ish
from __future__ import (absolute_import, division)
__metaclass__ = type

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import call, create_autospec
from ansible.module_utils.basic import AnsibleModule

from ansible.modules.extras.cloud.somebodyscomputer import firstmod


class TestFirstMod(unittest.TestCase):

    def test__save_data__happy_path(self):
        # Setup
        mod_cls = create_autospec(AnsibleModule)
        mod = mod_cls.return_value

        # Exercise
        firstmod.save_data(mod)

        # Verify
        self.assertEqual(1, mod.exit_json.call_count)

        expected = call(msg="Data saved", changed=True)
        self.assertEqual(expected, mod.exit_json.call_args)
