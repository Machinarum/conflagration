import wrap
from collections import namedtuple

def conflagration(files=None, dirs=None, recursive=False):
    dirs = dirs or list()
    dir_files = _parse_dirs(dirs, recursive=recursive)
    files.extend(dir_files)
    _superdict = dict()
    for d in [wrap.config_file(f) for f in files]:
        _superdict.update(d)
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

def _parse_dirs(dirs, recursive=False):
    files = []
    for d in dirs:
        for dirpath, directories, filenames in os.walk(d):
            files.extend([os.path.join(dirpath, f) for f in filenames])
    return files
