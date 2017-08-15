import unittest

from conflagration import namespace


class NamespaceTests(unittest.TestCase):


    def test_lowercasekeys(self):
        data = {
            'section1': {'key1': 'value1'},
            'SECTION1': {'key2': 'value2'},
            'Section2': {'another_key': 'another_value'}
        }
        lower_keys_func = namespace.LowerCaseKeys()
        lower_keys_func(data)
        assert data == {
            'section1': {'key1': 'value1', 'key2': 'value2'},
            'section2': {'another_key': 'another_value'}
        }