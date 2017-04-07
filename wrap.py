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
        clean_key = k.split(prefix)
        new_key = None
        if len(clean_key) > 1:
            new_key = clean_key[1]
        elif len(clean_key) == 1:
            new_key = clean_key[0]
        fdict[new_key] = filtered_vars[k]
    return fdict

# def environment(name='config', prefix='env.'):
#     env_vars = os.environ
#     filtered_vars = {
#         k: v for k, v in env_vars.iteritems() if k.startswith(prefix)
#     }
#     for k, v in filtered_vars.iteritems():
#         if not isidentifier(k):
#             logging.log(
#                 logging.ERROR,
#                 '{0} is not a valid proprty name.'.format(k))
#             raise Exception('{0} is not a valid proprty name.'.format(k))
#         else:
#             new_key = k.split(prefix)[1]
#             filtered_vars[new_key] = filtered_vars.pop(k)
#     return namedtuple(name, filtered_vars.keys())(**filtered_vars)
