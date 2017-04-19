import api

files = [
    'testconfigs/file1.config',
    'testconfigs/file2.config',
    'testconfigs/file3.config']

import os
env_vars = {
    "env.shared_section.envkey":"env1",
    "env.ENV_SECTION.key":"env1"}
os.environ.update(env_vars)

conf = api.conflagration(files=files, default_to_env=True)

for k,v in conf._asdict().items():
    print v
