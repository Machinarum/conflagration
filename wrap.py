import os
from ConfigParser import SafeConfigParser


class ConfigFileCollisionConflict(Exception):
    pass


def config_file(file, raise_conflicts=False):
    data = SafeConfigParser()
    data.read(file)
    ret = {}
    for s in data.sections():
        for k, v in data.items(s):
            key = '{}.{}'.format(s, k)
            if raise_conflicts and key in ret and ret.get(key) != v:
                raise ConfigFileCollisionConflict
            ret[key] = v
    return ret


def environment(prefix='env.'):
    env_vars = os.environ
    filtered_vars = {
        k: v for k, v in env_vars.iteritems() if k.startswith(prefix)
    }
    fdict = {}
    for k, v in filtered_vars.iteritems():
        _keysplit = k.split(prefix)
        new_key = None
        if len(_keysplit) > 1:
            new_key = _keysplit[1]
        elif len(_keysplit) == 1:
            new_key = _keysplit[0]
        fdict[new_key] = filtered_vars[k]
    return fdict
