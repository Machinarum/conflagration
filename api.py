from conflagration import wrap
from collections import namedtuple

class Conflagration(object):
    def __init__(
            self, files=None, dirs=None, recursive=False, include_env=True):
        fir_files = self._parse_dirs(*dirs, recurive=recursive)
        _config_wrappers = [wrap.config_file(f) for f in files]
        _env_wrapper = wrap.environment()

    def _parse_dirs(*dirs, recursive=False):
        files = 

        pass
        # smash all these data sources together and
        # return a Conflagration that's been initialized with that
        # file list.
