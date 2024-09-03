import os
from setuptools import setup, find_packages

def read_requirements(file_name: str) -> list:
    with open(file_name, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]

here = os.path.abspath(os.path.dirname(__file__))

# It's good practice to explicitly close the file, or use a context manager
with open(os.path.join(here, 'README.md'), 'r') as readme_file:
    long_description = readme_file.read()

requirements = read_requirements(os.path.join(here, 'requirements.txt'))

setup(
    name="orchard-litchi",
    version="0.1.1",
    packages=find_packages(exclude=["tests*"]),
    include_package_data = True,
    package_data = {
        '': ['*.prompt'],
    },
    install_requires=requirements,
    author="Orchard Universe",
    description="Litchi is yet another coding assistant powered by LLM.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OrchardUniverse/litchi",
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
