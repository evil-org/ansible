# Make coding more python3-ish
from __future__ import (absolute_import, division)
__metaclass__ = type

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import call, create_autospec, patch
from ansible.module_utils.basic import AnsibleModule

from ansible.modules.extras.cloud.somebodyscomputer import firstmod


class TestFirstMod(unittest.TestCase):

    @patch('ansible.modules.extras.cloud.somebodyscomputer.firstmod.write')
    @patch('ansible.modules.extras.cloud.somebodyscomputer.firstmod.fetch')
    def test__save_data__happy_path(self, fetch, write):
        # Setup
        mod_cls = create_autospec(AnsibleModule)
        mod = mod_cls.return_value
        mod.params = dict(
            url="https://www.google.com",
            dest="/tmp/firstmod.txt"
        )

        write.return_value = True

        # Exercise
        firstmod.save_data(mod)

        # Verify
        self.assertEqual(1, mod.exit_json.call_count)

        expected = call(msg="Data saved", changed=True)
        self.assertEqual(expected, mod.exit_json.call_args)

        self.assertEqual(1, fetch.call_count)

        expected = call(mod.params["url"])
        self.assertEqual(expected, fetch.call_args)

        self.assertEqual(1, write.call_count)

        expected = call(fetch.return_value, mod.params["dest"])
        self.assertEqual(expected, write.call_args)

    @patch('ansible.modules.extras.cloud.somebodyscomputer.firstmod.write')
    @patch('ansible.modules.extras.cloud.somebodyscomputer.firstmod.fetch')
    def test__save_data__failure(self, fetch, write):
        # Setup
        mod_cls = create_autospec(AnsibleModule)
        mod = mod_cls.return_value
        mod.params = dict(
            url="https://www.google.com",
            dest="/tmp/firstmod.txt"
        )

        write.return_value = False

        # Exercise
        firstmod.save_data(mod)

        # Verify
        self.assertEqual(1, mod.fail_json.call_count)

        expected = call(msg="Data could not be saved")
        self.assertEqual(expected, mod.fail_json.call_args)

        self.assertEqual(1, fetch.call_count)

        expected = call(mod.params["url"])
        self.assertEqual(expected, fetch.call_args)

        self.assertEqual(1, write.call_count)

        expected = call(fetch.return_value, mod.params["dest"])
        self.assertEqual(expected, write.call_args)
