try:
    # Python 3
    from types import SimpleNamespace as _Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace as _Namespace


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


class _BaseNamespaceModifier(object):
    __metaclass__ = _ModifierRegistrar


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
        for k in original_dict.keys():
            if k.lower() != k:
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
