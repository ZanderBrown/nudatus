#!/usr/bin/env python3
from setuptools import setup
from nudatus import get_version


with open('README.rst') as f:
    readme = f.read()
with open('CHANGES.rst') as f:
    changes = f.read()


setup(
    name='nudatus',
    version=get_version(),
    description='Strip comments from scripts, intended for use with '
                'MicroPython and other storage constrained '
                'environments',
    long_description=readme + '\n\n' + changes,
    author='Zander Brown',
    url='https://github.com/zanderbrown/nudatus',
    py_modules=['nudatus', ],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts': ['nudatus=nudatus:main'],
    }
)
