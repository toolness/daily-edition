from setuptools import setup

from dev.bootstrap import install_requires

setup(
    name='daily_edition',
    version='0.1',
    packages=['daily_edition'],
    author='Atul Varma',
    author_email='varmaa@toolness.com',
    install_requires=install_requires
    )
