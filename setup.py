from setuptools import setup

setup(
    name='daily_edition',
    version='0.1',
    packages=['daily_edition'],
    author='Atul Varma',
    author_email='varmaa@toolness.com',
    install_requires=['django==1.3', 'feedparser==5.0.1', 'simplejson']
    )
