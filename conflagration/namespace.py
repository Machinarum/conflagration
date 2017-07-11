try:
    # Python 3
    from types import SimpleNamespace as _Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace as _Namespace


class _NamespaceDict(_Namespace):
    def __getitem__(self, item):
        return self.__dict__[item]


def namespace_hook(d):
    """Corrects an issue where keys named 'self' cause this to error."""
    if 'self' in d.keys():
        d['self_'] = d['self']
        del d['self']
    return _NamespaceDict(**d)


# ############Code below here is experimental ##############
# Global registry of all namspace modifiers
modifiers = _NamespaceDict()


class _ModifierRegistrar(type):

    def __new__(cls, clsname, bases, attrs):
        modclass = super(_ModifierRegistrar, cls).__new__(
            cls, clsname, bases, attrs)
        global modifiers
        modifiers.__dict__[clsname] = modclass
        return modclass


class KeyMapper(object):
    __metaclass__ = _ModifierRegistrar
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


def namespace(original_dict, modifier=None):
    """
    TODO: This won't work if fed into json's object hook, so it can't be used
    in place of the NamespaceDict directly yet.

    Factory method for generating namespace objects.
    Optionally allowes for providing a modifer function to act of the
    original_dict before being turned into a namespace object.
    """
    if modifier:
        modifier(original_dict)

    # Apply default 'self' modification in case user provided modifer doesn't.
    if 'self' in original_dict:
        modifiers.KeyMapper({'self': 'self_'})(original_dict)

    return _NamespaceDict(**original_dict)
