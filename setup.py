#!/usr/bin/env python

import os
import setuptools

VERSION = '0.3.1'

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setuptools.setup(
    name='glog',
    author='Benjamin Staffin',
    author_email='benley@gmail.com',
    url='https://github.com/benley/python-glog',
    install_requires=[
        'python-gflags>=3.1',
        'six',  # glog doesn't need six, but gflags 3.1 does and its distutils
                # "requires" line apparently accomplishes nothing, so ...
    ],
    description='Simple Google-style logging wrapper for Python.',
    long_description=README,
    py_modules=['glog'],
    license='BSD',
    test_suite='tests',
    version=VERSION,
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: System :: Logging',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms='any',
)
