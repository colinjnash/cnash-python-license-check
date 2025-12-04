"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# To use a consistent encoding
from codecs import open
from os import path, environ

# Always prefer setuptools over distutils
from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "readme.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="liccheck",
    # Versions should comply with PEP440.
    # UPDATED to 4.0.1 to force CI update
    version="4.0.1",
    description="Check python packages from requirement.txt and report issues",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # UPDATED to your fork
    url="https://github.com/colinjnash/cnash-python-license-check",
    # UPDATED Author details
    author="Colin Nash",
    author_email="colinjnash@gmail.com",
    # Choose your license
    license="Apache Software License",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: Apache Software License",
        # Specify the Python versions you support here.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    # What does your project relate to?
    keywords="license check build tool",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=["liccheck"],
    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],
    python_requires=">=3.5",
    install_requires=["semantic_version>=2.7.0", "toml"],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        "console_scripts": ["liccheck=liccheck.command_line:main"],
    },
)
