import unittest

from conflagration import namespace


class NamespaceTests(unittest.TestCase):

    def test_exception_on_overwrite(self):
        data = {
            'section1': {'key1': 'value1'},
            'SECTION1': {'key2': 'value2'}
        }
        lower_keys_func = namespace.LowerCaseKeys()
        with self.assertRaises(Exception):
            lower_keys_func(data)
    
    def test_lowercasekeys_upper_key(self):
        data = {
            'section1': {'key1': 'value1'},
            'SECTION2': {'key2': 'value2'}
        }
        original_data = data.copy()
        lower_keys_func = namespace.LowerCaseKeys()
        lower_keys_func(data)
        assert data == {
            'section1': {'key1': 'value1'},
            'section2': {'key2': 'value2'}
        }
    
    def test_lowercasekeys_all_lower(self):
        data = {
            'section1': {'key1': 'value1'},
            'section2': {'key2': 'value2'}
        }
        original_data = data.copy()
        lower_keys_func = namespace.LowerCaseKeys()
        lower_keys_func(data)
        assert data == {
            'section1': {'key1': 'value1'},
            'section2': {'key2': 'value2'}
        }
