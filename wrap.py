from ConfigParser import SafeConfigParser
from collections import namedtuple
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
