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

    @mock.patch("conflagration.api.namedtuple")
    def test_dict_to_nt_flat_dict(self, mnt):
        mnt.return_value = dict
        data = {'key': 'value'}
        r = api._dict_to_nt(data, 'name')
        self.assertEqual(data, r)


    @mock.patch("conflagration.api.namedtuple")
    def test_dict_to_nt_nested_dict(self, mnt):
        mnt.return_value = dict
        data = {'key': {'subkey':'value'}}
        r = api._dict_to_nt(data, 'name')
        self.assertEqual(data, r)

    @mock.patch("conflagration.api._dict_to_nt")
    @mock.patch("conflagration.api._dotstring_to_nested_dict")
    def test_build_super_namedtuple(self, mdtnd, mdtn):
        inputd = {'key.subkey':'VALUE0'}
        mdtnd.return_value = 'VALUE1'
        mdtn.return_value = 'VALUE2'
        r = api._build_super_namedtuple(inputd, 'name')

        self.assertEqual(r, 'VALUE2')

        mdtnd.assert_called_once_with(
            return_dict=dict(),
            splitkey_list=['key', 'subkey'],
            value='VALUE0')

        mdtn.assert_called_once_with(source_dict=dict(), name='name')

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
