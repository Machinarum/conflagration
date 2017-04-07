import wrap
from collections import namedtuple


class ConflictException(Exception):
    pass

def conflagration(
        files=None, dirs=None, recurse_dirs=False,
        allow_env_override=True, default_to_env=False,
        raise_on_conflicts=True):
    """
    Will collect all configs at all file paths discovered in 'dirs' and
    those in 'files', parse them, and combine them in a named tuple.
    The load order of the files is not guaranteed.

    if recurse_dirs is True, all files in all sub directories in all
    directories in 'dirs' will be included in the final namedtuple.

    If allow_env_override is True (default) any environment variable that
    matches the 'env.section.key=value' pattern will override any matching
    key/value pair provided in any config.

    If default_to_env is True (default) any environment variable that
    matches the 'env.section.key=value' pattern will be used as the default
    value for that key, but will be overridden by any matching key/value
    pair provided in any config.

    If raise_on_conflicts is True (default), a ConflictException will be
    raised if any two configs files hold differing values for the same
    key/value pair in a shared section name
    """
    dirs = dirs or list()
    dir_files = _parse_dirs(dirs, recurse_dirs=recurse_dirs)
    files.extend(dir_files)
    _superdict = dict()
    _envdict = wrap.environment()

    if default_to_env:
        _superdict.update(_envdict)

    for d in [wrap.config_file(f) for f in files]:
        _superdict.update(d)

    if allow_env_override:
        _superdict.update(_envdict)

    return _build_super_namedtuple(_superdict, 'conflagration')

def _dotstring_to_nested_dict(dic, key, value):
    k = key[0]
    if len(key) > 1:
        klist = key[1::]
        if k in dic:
            _dotstring_to_nested_dict(dic[k], klist, value)
        else:
            dic[k] = _dotstring_to_nested_dict(dict(), klist, value)
    elif len(key) == 1:
        dic[k] = value
    return dic

def _dict_to_nt(d, name):
    keys = d.keys()
    finald = dict()
    for k in keys:
        if isinstance(d[k], dict):
            finald[k] = _dict_to_nt(d[k], k)
        else:
            finald[k] = d[k]
    return namedtuple(name, finald.keys(), verbose=True)(**finald)

def _build_super_namedtuple(superdict, name):
    nested_superdict = dict()
    for k, v in superdict.items():
        _dotstring_to_nested_dict(nested_superdict, k.split('.'), v)
    return _dict_to_nt(nested_superdict, name)

def _parse_dirs(dirs, recurse_dirs=False):
    files = []
    for d in dirs:
        for dirpath, directories, filenames in os.walk(d):
            files.extend([os.path.join(dirpath, f) for f in filenames])
    return files
