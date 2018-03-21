from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='jw-pylib',
    version='1.0.0',

    description='Some useful python utils',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/jaggerwang/jw-pylib',
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/jaggerwang/jw-pylib/issues',
        'Source': 'https://github.com/jaggerwang/jw-pylib',
    },

    author='Jagger Wang',
    author_email='jaggerwang@gmail.com',

    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],

    keywords='utils',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    python_requires='>=3',
    install_requires=['requests', 'pycrypto'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
