import os

import six
from six.moves.configparser import SafeConfigParser


class ConfigFile(object):

    @staticmethod
    def read(cfgfile):
        if not os.path.exists(cfgfile):
            ex = IOError if six.PY2 else FileNotFoundError
            raise ex('File {name} does not exist.'.format(name=cfgfile))
        data = SafeConfigParser()
        data.read(cfgfile)
        return data

    @staticmethod
    def generate_address(section, separator, key):
        return '{}{}{}'.format(section, separator, key)

    @staticmethod
    def parse(
            cfgfile, raise_conflicts=False, case_insensitive=False,
            separator="."):
        """
        Reads in a config file and convert is to a dictionary where each
        entry follows the pattern dict["section.key"]="value"
        """

        cfg = ConfigFile.read(cfgfile)
        address_dict = {}
        for s in cfg.sections():
            for k, v in cfg.items(s):
                key = ConfigFile.generate_address(s, separator, k)
                if case_insensitive:
                    key = key.lower()
                if raise_conflicts and key in address_dict.keys():
                    msg = (
                        "Duplicate section or key in config file {msg}: "
                        "\nFile: {f}\nSection: {s}\nKey: {k}".format(
                            msg='When case_insensitive=False' if
                                case_insensitive else '',
                            f=cfgfile,
                            s=s,
                            k=key))
                    raise Exception(msg)
                address_dict[key] = v
        return address_dict

    @staticmethod
    def write(cfg_obj, output_file_path):
        """
        Only supports writing out a conflagration object with namespaces that
        follow the section.key=value pattern that ConfigFile.parse generates
        """
        parser = SafeConfigParser()
        for k in cfg_obj.__dict__.keys():
            parser.add_section(k)
            try:
                for sub_k, sub_v in cfg_obj.__dict__[k].__dict__.items():
                    parser.set(k, sub_k, sub_v)
            except Exception:
                raise Exception(
                    "Output to config file not supported for conflagrations"
                    "nested beyond a one dot namespace.")

        with open(output_file_path, 'w') as f:
            parser.write(f)

    @staticmethod
    def multiparse(
            file_list, raise_conflicts=False, case_insensitive=False,
            separator="."):
        """
        Reads in one or more config files and converts their content to a
        dictionary, raising an error on key conflicts.
        The keys will be equal to the section_name
        """
        aggregate_dict = dict()

        # Parse each file to a dictionary, and update the data dict with its
        # contents.
        for f in file_list:
            cfg_dict = ConfigFile.parse(
                f,
                raise_conflicts=raise_conflicts,
                case_insensitive=case_insensitive,
                separator=separator)

            # If any key exists in the aggregate dict and the config file dict,
            # raise an exception if the values aren't identical.
            if raise_conflicts:
                intersection = set(cfg_dict.keys()).intersection(
                    set(aggregate_dict.keys()))
                for i in intersection:
                    if cfg_dict[i] != aggregate_dict[i]:
                        raise Exception(
                            "At least two of the files passed in file_list"
                            " define a different value for the same key in the"
                            " same section")
            aggregate_dict.update(cfg_dict)
        return aggregate_dict


class Env(object):

    @staticmethod
    def parse(prefix='env', separator="__", case_insensitive=False):
        """
        Returns a dictionary of all relavent environment variables and their
        values, with the prefix stripped from the keys.
        """

        filtered_vars = Env.filter(
            prefix=prefix,
            separator=separator,
            case_insensitive=case_insensitive)

        data = {}
        if case_insensitive:
            prefix = prefix.lower()

        for k, v in six.iteritems(filtered_vars):
            _keysplit = k.split("{}{}".format(prefix, separator))
            new_key = None
            if len(_keysplit) > 1:
                new_key = _keysplit[1]
            elif len(_keysplit) == 1:
                new_key = _keysplit[0]

            # The rest of the codebase expects the separator to be a dot by
            #  default, but env vars can't have dots in the name.
            new_key = new_key.replace(separator, ".")
            data[new_key] = filtered_vars[k]

        return data

    @staticmethod
    def filter(prefix='env', separator="__", case_insensitive=False):
        """
        Returns environment variable dictionary for env vars starting with
        the provided prefix and separator
        """
        pfx = "{}{}".format(prefix, separator)
        data = dict()
        if case_insensitive:
            for k, v in six.iteritems(os.environ):
                if k.startswith(pfx):
                    if k.lower() in os.environ \
                            and os.environ.get(k.lower()) != os.environ.get(k):
                        # The lower version of this key would conflict with
                        # another key in the env
                        raise Exception(
                            'Lowercasing keys would result in dataloss. '
                            'Upper case key {uk}={ukv} would overlap with '
                            'lowercase key that has a different value '
                            '({lk}={lkv})'.format(
                                uk=k,
                                ukv=os.environ.get(k),
                                lk=k.lower(),
                                lkv=os.environ.get(k.lower())))
                    data[k.lower()] = v

        else:
            data = {
                k: v for k, v in six.iteritems(os.environ) if k.startswith(pfx)}
        return data

    @staticmethod
    def export_shellscript(
            cfg_obj, output_file_path=None, shell='bash', prefix='env',
            separator="__"):
        if shell != 'bash':
            "Non-bash shells are not supported"

        lines = ["# bash export file generated by conflagration"]
        for k in cfg_obj.__dict__.keys():
            try:
                for sub_k, sub_v in cfg_obj.__dict__[k].__dict__.items():
                    lines.append(
                        "\nexport "
                        "{prefix}{sep}{key}{sep}{subkey}={value}".format(
                            prefix=prefix, sep=separator, key=k, subkey=sub_k,
                            value=sub_v))
            except Exception:
                raise Exception(
                    "Output to shell script not supported for conflagrations"
                    "nested beyond a one dot namespace.")
        if output_file_path:
            with open(output_file_path, 'w') as f:
                f.writelines(lines)
        else:
            for line in lines:
                print(line)
