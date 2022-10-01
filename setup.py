import re
import sys
from os import path
from setuptools import setup, find_packages

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

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
    name='TLVParkingAPI',
    version=version,
    python_requires='~=3.7',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/ShahafEdri/TLVParkingAPI',
    project_urls={
        'Source': 'https://github.com/ShahafEdri/TLVParkingAPI',
    },
    include_package_data=True,
    install_requires=requirements,
    license='Shahaf Edri',
    author='Shahaf Edri',
    description="",
    long_description="",
    
)

if __name__ == "__main__":
    pass
