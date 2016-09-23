# Make coding more python3-ish
from __future__ import (absolute_import, division)
__metaclass__ = type

from urllib2 import URLError

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import call, create_autospec, patch
from ansible.module_utils.basic import AnsibleModule

from ansible.modules.extras.cloud.somebodyscomputer import firstmod


class TestFirstMod(unittest.TestCase):

    @patch('ansible.modules.extras.cloud.somebodyscomputer.firstmod.open_url')
    def test__fetch__happy_path(self, open_url):
        # Setup
        url = "https://www.google.com"

        # mock the return value of open_url
        stream = open_url.return_value
        stream.read.return_value = "<html><head></head><body>Hello</body></html>"
        stream.getcode.return_value = 200
        open_url.return_value = stream

        # Exercise
        data = firstmod.fetch(url)

        # Verify
        self.assertEqual(stream.read.return_value, data)

        self.assertEqual(1, open_url.call_count)

        expected = call(url)
        self.assertEqual(expected, open_url.call_args)

    @patch('ansible.modules.extras.cloud.somebodyscomputer.firstmod.open_url')
    def test__fetch__not_found(self, open_url):
        # Setup
        url = "http://blahblah.non.existent"

        open_url.side_effect = URLError("Unknown URL")

        # Exercise
        with self.assertRaises(URLError):
            firstmod.fetch(url)

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
    def test__save_data__fetch_failure(self, fetch, write):
        # Setup
        mod_cls = create_autospec(AnsibleModule)
        mod = mod_cls.return_value
        mod.params = dict(
            url="https://www.google.com",
            dest="/tmp/firstmod.txt"
        )

        fetch.side_effect = URLError("Unknown URL")

        # Exercise
        firstmod.save_data(mod)

        # Verify
        self.assertEqual(1, mod.fail_json.call_count)

        expected = call(msg="Data could not be retrieved")
        self.assertEqual(expected, mod.fail_json.call_args)

        self.assertEqual(1, fetch.call_count)

        expected = call(mod.params["url"])
        self.assertEqual(expected, fetch.call_args)

        self.assertEqual(0, write.call_count)

    @patch('ansible.modules.extras.cloud.somebodyscomputer.firstmod.write')
    @patch('ansible.modules.extras.cloud.somebodyscomputer.firstmod.fetch')
    def test__save_data__write_failure(self, fetch, write):
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
