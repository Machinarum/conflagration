import unittest
import mock
import os
from conflagration import api

class Fixture(unittest.TestCase):
    pass

class Test_parse_dirs(Fixture):

    def test_parse_dirs_returns_empty_list_on_empty_dir_list(self):
        r = api._parse_dirs([])
        self.assertIsInstance(r, list)
        self.assertEqual(r, list())

    def test_dotstring_to_nested_dict_dotted_key(self):
        test_dict = {}
        expected = {'key':{'subkey':'value'}}
        r = api._dotstring_to_nested_dict(
            test_dict, ['key', 'subkey'], 'value')
        self.assertEqual(expected, r)

    def test_dotstring_to_nested_dict_flat_key(self):
        test_dict = {}
        expected = {'key':'value'}
        r = api._dotstring_to_nested_dict(
            test_dict, ['key'], 'value')
        self.assertEqual(expected, r)

    def test_dotstring_to_nested_dict_dotted_existing_key(self):
        test_dict = {'key': {'subkey':'value0'}}
        expected = {'key':{'subkey':'value1'}}
        r = api._dotstring_to_nested_dict(
            test_dict, ['key', 'subkey'], 'value1')
        self.assertEqual(expected, r)

    def test_dotstring_to_nested_dict_flat_existing_key(self):
        test_dict = {'key': 'value0'}
        expected = {'key':'value1'}
        r = api._dotstring_to_nested_dict(
            test_dict, ['key'], 'value1')
        self.assertEqual(expected, r)

    def test_build_namespace(self):
        address_dict = {'key.subkey':'VALUE0'}
        separator="."
        r = api._build_namespace(address_dict, separator)
        self.assertEqual(r.key.subkey, "VALUE0" )

    @mock.patch("conflagration.api.os.walk")
    def test_parse_dirs_returns_file_list_for_multiple_dirs(self, mockwalk):
        mockwalk.return_value = [('dirpath1', [], ['file1', 'file2'],),]
        expected = []
        expected.extend(
            [os.path.join('dirpath1', 'file1'),
             os.path.join('dirpath1', 'file2')])
        expected.extend(
            [os.path.join('dirpath1', 'file1'),
             os.path.join('dirpath1', 'file2')])

        files = api._parse_dirs(['dirpath1', 'dirpath2'])
        self.assertEqual(mockwalk.call_count, 2)
        self.assertEqual(expected, files)
