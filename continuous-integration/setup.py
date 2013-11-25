try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Various utilities for Infrared5 dev-ops.',
    'author': 'Infrared5',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'todd@infrared5.com',
    'version': '0.1.0',
    'install_requires': ['nose', 'lettuce', 'pylint'],
    'packages': ['ci.jenkins', 'ci.teamcity'],
    'scripts': [],
    'name': 'dev-ops'
}

setup(**config)
