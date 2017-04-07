from ConfigParser import SafeConfigParser
import logging
import os


def config_file(file):
    data = SafeConfigParser()
    data.read(file)
    section_dict = {}
    for s in data.sections():
        for k, v in data.items(s):
            section_dict['{}.{}'.format(s,k)]=v
    return section_dict

def environment(prefix='env.'):
    env_vars = os.environ
    filtered_vars = {
        k: v for k, v in env_vars.iteritems() if k.startswith(prefix)
    }
    fdict={}
    for k, v in filtered_vars.iteritems():
        _keysplit = k.split(prefix)
        new_key = None
        if len(_keysplit) > 1:
            new_key = _keysplit[1]
        elif len(_keysplit) == 1:
            new_key = _keysplit[0]
        fdict[new_key] = filtered_vars[k]
    return fdict
