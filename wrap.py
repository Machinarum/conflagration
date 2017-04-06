from ConfigParser import SafeConfigParser
from collections import namedtuple
from future.utils import isidentifier
import logging
import os
import prettyprint


def config_file(file, name=None):
    _data = SafeConfigParser()
    _data.read(file)
    sect_nts = {}
    for s in _data.sections():
        s_dict = {k: v for (k, v) in _data.items(s)}
        nt = namedtuple(s, s_dict.keys())(**s_dict)
        sect_nts[s]=nt
    return namedtuple(
        name or 'config', sect_nts.keys())(**sect_nts)


def environment(name='config', prefix='ENV_'):
    env_vars = os.environ
    filtered_vars = {
        k: v for k, v in env_vars.iteritems() if k.startswith(prefix)
    }
    for k, v in filtered_vars.iteritems():
        if not isidentifier(k):
            logging.log(
                logging.ERROR,
                '{0} is not a valid proprty name.'.format(k))
            raise Exception('{0} is not a valid proprty name.'.format(k))
        else:
            new_key = k.split(prefix)[1]
            filtered_vars[new_key] = filtered_vars.pop(k)
    return namedtuple(name, filtered_vars.keys())(**filtered_vars)
