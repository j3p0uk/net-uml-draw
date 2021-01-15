__author__ = 'j3p0uk'

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
version_file = os.path.join(here, 'VERSION')

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

if not os.path.isfile(version_file):
    BUILD_NUMBER = os.environ.get('GITHUB_RUN_NUMBER', '0')
    with open(version_file, encoding='utf-8', mode='w') as f:
        f.write(BUILD_NUMBER)
else:
    with open(version_file, encoding='utf-8') as f:
        BUILD_NUMBER = f.read().strip()

setup(
    name='net_uml_draw',
    version='2.' + BUILD_NUMBER,

    description='Write PlantUML from a Google Sheet network description',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/j3p0uk/net-uml-draw',

    author='JP Sullivan (j3p0uk)',
    author_email='j3p0uk@gmail.com',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='network_diagram plantuml google_sheets',

    install_requires=[
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "numpy"
    ],

    platforms=['Any'],

    scripts=[],

    provides=['net_uml_draw'],

    packages=find_packages(exclude=['docs', 'test']),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'net-uml-draw=net_uml_draw.cli:main',
        ],
    },

    data_files=[("", ["LICENSE", "VERSION"])],

    project_urls={
        'Bug Reports': 'https://github.com/j3p0uk/net-uml-draw/issues',
        'Source': 'https://github.com/j3p0uk/net-uml-draw/',
    },

    zip_safe=False,
)
