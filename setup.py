from setuptools import setup, find_packages

setup(
    version='0.0.6',
    name='conflagration',
    author='dwalleck and jidar',
    author_email='core.machinarum@gmail.com',
    install_requires=['six'],
    packages=find_packages(exclude=('tests', 'docs')),
    package_dir={'conflagration': 'conflagration'},
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ))
