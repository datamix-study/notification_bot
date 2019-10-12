import os

from setuptools import setup


def read_requirements():
    path = os.path.join(__file__, '..', 'requirements.txt')
    with path as f:
        requirements = f.read().splitlines()
    return requirements


setup(
    name='notification_bot',
    version='0.0.1',
    packages=[''],
    url='',
    license='',
    author='datamix-study',
    author_email='',
    description='This is a bot that sends notifications about Datamix.',
    install_requires=read_requirements()
)
