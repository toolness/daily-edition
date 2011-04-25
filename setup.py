from setuptools import setup

from manage import req_contents

setup(
    name='daily_edition',
    version='0.1',
    packages=['daily_edition'],
    author='Atul Varma',
    author_email='varmaa@toolness.com',
    install_requires=req_contents.split()
    )
