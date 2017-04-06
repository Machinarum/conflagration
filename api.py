from conflagration import wrap
from collections import namedtuple

def conflagrate(*files):
    nts = [wrap.config_file(f) for f in files]
    print nts._asdict().keys()
    #self._data = namedtuple('conflagration', nts._asdict().keys())

def conf(files=None, dirs=None, recursive=False):
    pass
    # smash all these data sources together and
    # return a Conflagration that's been initialized with that
    # file list.
