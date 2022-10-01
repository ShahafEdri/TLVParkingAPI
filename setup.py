import re
import sys
from os import path
from setuptools import setup, find_packages

requirements = [
    'flask==2.2',
    'request',
    'bs4',
    'lxml',
]

version_file = path.join(
    path.dirname(__file__),
    'flaskr',
    '__version__.py'
)

with open(version_file, 'r') as fp:
    m = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        fp.read(),
        re.M
    )
    version = m.groups(1)[0]

setup(
    name='tlv-parking-lots-tonnage-flask',
    version=version,
    packages=find_packages(exclude=['tests']),
    url='https://www.github.com/flask-restful/flask-restful/',
    project_urls={
        'Source': 'https://github.com/flask-restful/flask-restful',
    },
    include_package_data=True,
    install_requires=requirements,
    license='Shahaf Edri',
)

if __name__ == "__main__":
    pass
