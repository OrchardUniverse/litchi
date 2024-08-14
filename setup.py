import os
from setuptools import setup, find_packages

def read_requirements(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]
here = os.path.abspath(os.path.dirname(__file__))
requirements = read_requirements(os.path.join(here, 'requirements.txt'))

setup(
    name="litchi",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    install_requires=requirements,
    author="Orchard Universe",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'litchi=litchi.cli.main:cli',
        ],
    },
)
