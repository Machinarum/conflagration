import os
import json
from conflagration import wrap, namespace

"""
Conflagration takes multiple key/value sources and derives a
'conflagration address key' for each key/value pair in each source, and
returns a single interface for them.

Sources can be specially crafted such that multiple sources can be used
together, and even be used to override eachother (such as environment
variables overriding config file key/value pairs)

Examples:

    Given:
        file1.conf
            [section_a]
            key=1

            [shared_section]
            f1key=2

        file2.conf
            [section_b]
            key=3

            [shared_section]
            f2key=4

    One File:
        cfg = conflagration(["file1.conf"])
        print cfg.section_a.key
        >> 1

    default_to_env is True, allow_env_override is False:
        os.environ['env.section_a.key'] = 'ENV_A'
        os.environ['env.section_c.key'] = 'ENV_C'
        cfg = conflagration(["file1.conf"])
        print cfg.section_a.key
        >> 1
        print cfg.section_c.key
        >> 'ENV_C'

    default_to_env if False, allow_env_override is True:
        os.environ['env.section_a.key'] = 'ENV_A'
        os.environ['env.section_c.key'] = 'ENV_C'
        cfg = conflagration(["file1.conf"])
        print cfg.section_a.key
        >> 'ENV_A'
        print cfg.section_c.key
        >> AttributeError: 'conflagration' object has no attribute 'section_c'

    default_to_env if True, allow_env_override is True:
        os.environ['env.section_a.key'] = 'ENV_A'
        os.environ['env.section_c.key'] = 'ENV_C'
        cfg = conflagration()
        print cfg.section_a.key
        >> 'ENV_A'
        print cfg.section_c.key
        >> 'ENV_C'

    Two files
        cfg = conflagration(["file1.conf", "file2.conf"])
        print cfg.section_a.key
        >> 1
        print cfg.section_b.key
        >> 3
        print cfg.shared_section.f1key
        >> 2
        print cfg.shared_section.f2key
        >> 4
"""


def conflagration(
        files=None, dirs=None, allow_env_override=True, default_to_env=False,
        raise_conflicts=True, env_var_prefix='env', env_var_separator='__',
        lowercase_keys=False, namespace_obj=None):
    """
    :param files: A list of paths to config files.
    :param dirs: A list of directories that is presumed to contain only config
                 files
    :param allow_env_override: If True, sets the value of all conflagration
        address keys to corresponding environment variables, ignoring
        other sources if a corresponding env var exists.
    :param default_to_env: If True, defaults the value of all conflagration
        address keys to corresponding environment variables, allowing other
        sources to override the environment variables.
    :param raise_conflicts: If True, raises an exception if conflicting values
        exist for the same conflagration address key among all config files.
    :param env_var_prefix: conflagration will expect env vars to start with
        this string
    :param env_var_separator: conflagration will expect env var keys to follow
        the "prefix<sep>section<sep>key" pattern where <sep> is this string.
    :param lowercase_keys: If True, conflagration will automatically lowercase
        all keys in the final namespace object.
    :param namespace_obj:You can pass in a custom ModifiableNamespace object
        as created via the ModifiableNamespace class in conflagration.namespace
        By default, the namespace object will lowercase all keys.  If you pass
        one in, it will override the lowercase_keys flag.
    """

    #TODO: Make the interaction between the default ns behavior and a custom ns
    #      less clunky

    files = files or list()
    dirs = dirs or list()
    dir_files = _parse_dirs(dirs)
    files.extend(dir_files)

    _filedict = wrap.ConfigFile.multiparse(
        file_list=files,
        raise_conflicts=raise_conflicts)

    _envdict = wrap.Env.parse(
        prefix=env_var_prefix,
        separator=env_var_separator)

    if default_to_env:
        _envdict.update(_filedict)

    if allow_env_override:
        _filedict.update(_envdict)

    if not namespace_obj:
        mods = [namespace.modifiers.KeyMapper({'self': 'self_'})]
        if lowercase_keys:
            modifier_list.insert(0, namespace.modifiers.LowerCaseKeys())
        namespace_obj = namespace.ModifiableNamespace(modifier_list=mods)

    return _build_namespace(
        address_dict=_filedict, namespace_obj=namespace_obj)


def _dotstring_to_nested_dict(return_dict, splitkey_list, value):
    """Replaces the value for the key in return_dict corresponding to the
    first element in splitkey_list with a dictionary containing either the
    provided value, or another dictionary containing the next element in the
    split key list.  It will recurse doing this until there are no elements
    left in the split key list.

    Overrides existing values for duplicate key addresses with last
    discovered value for that key address

    Example:
        Given
            splitkey_list = ['this', 'is', 'a', 'key']
            'value'='value'
            return_dict = {}
        Result
            return_dict['this']={'is': {'a': {'key': 'value'}}}
    """
    k = splitkey_list[0]
    if len(splitkey_list) > 1:
        klist = splitkey_list[1::]
        if k in return_dict:
            _dotstring_to_nested_dict(
                return_dict=return_dict[k],
                splitkey_list=klist,
                value=value)
        else:
            return_dict[k] = _dotstring_to_nested_dict(
                return_dict=dict(),
                splitkey_list=klist,
                value=value)

    elif len(splitkey_list) == 1:
        return_dict[k] = value
    return return_dict


def _build_namespace(address_dict, separator='.', namespace_obj=None):
    nested_address_dict = dict()
    namespace_obj = namespace_obj or namespace.ModifiableNamespace()
    for k, v in address_dict.items():
        _dotstring_to_nested_dict(
            return_dict=nested_address_dict,
            splitkey_list=k.split(separator),
            value=v)

    jdict = json.dumps(nested_address_dict)
    return json.loads(jdict, object_hook=namespace_obj)


def _parse_dirs(dirs):
    files = []
    for d in dirs:
        for dirpath, directories, filenames in os.walk(d):
            files.extend([os.path.join(dirpath, f) for f in filenames])
    return files
