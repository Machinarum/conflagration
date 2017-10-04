try:
    # Python 3
    from types import SimpleNamespace as _Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace as _Namespace

from six import with_metaclass

class _NamespaceDict(_Namespace):
    def __getitem__(self, item):
        return self.__dict__[item]


modifiers = _NamespaceDict()


class _ModifierRegistrar(type):

    def __new__(cls, clsname, bases, attrs):
        modclass = super(_ModifierRegistrar, cls).__new__(
            cls, clsname, bases, attrs)
        global modifiers
        modifiers.__dict__[clsname] = modclass
        return modclass


class _BaseNamespaceModifier(with_metaclass(_ModifierRegistrar)):
    pass

class KeyMapper(_BaseNamespaceModifier):
    """Given key_remapping_dict, replaces all keys in original_dict with the
    value of the corresponding key in key_remapping_dict.
    By default, it will also remap self to self_ to prevent issues with the
    NamespaceDict object.
    """

    def __init__(self, key_remapping_dict=None):
        self.key_remapping_dict = key_remapping_dict or dict()

    def __call__(self, original_dict):
        for k in self.key_remapping_dict.keys():
            if k in original_dict:
                original_dict[self.key_remapping_dict[k]] = original_dict[k]
                del original_dict[k]


class LowerCaseKeys(_BaseNamespaceModifier):
    """Automatically lowercases all keys in the original dictionary.
    """

    def __call__(self, original_dict):
        keylist = original_dict.keys()
        for k in keylist:
            if (k.lower() in original_dict) \
                    and (original_dict[k.lower()] != original_dict[k]):
                # An upper case k/v pair would overwrite an existing
                # lower case k/v pair if
                raise Exception(
                    'Lowercasing keys would result in dataloss. Uppercase '
                    'key {uk}={ukv} would overlap with lowercase key that has '
                    'a different value ({lk}={lkv})'.format(
                        uk=k,
                        ukv=original_dict[k],
                        lk=k.lower(),
                        lkv=original_dict[k.lower()]))
            elif k.lower() in original_dict:
                # The lower version exists but contains the same key.
                # delete the upper case version and move on.
                del original_dict[k]
            elif k.lower() not in original_dict:
                # The lowercase version of the current key would be a new
                # unique key.  Save the new lower version and delete the old
                original_dict[k.lower()] = original_dict[k]
                del original_dict[k]


class ModifiableNamespace(object):
    """
    Returns an object function for use in the _build_namespace function
    hook_list should be a subset of the hooks in the global 'modifiers'
    attribute from this module.
    """
    def __init__(self, modifier_list=None):
        self.modifiers = modifier_list or list()

    def __call__(self, original_dict):
        for mod in self.modifiers:
            mod(original_dict)
        return _NamespaceDict(**original_dict)
