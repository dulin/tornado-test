from setuptools import setup, find_packages

requires = [
    "tornado",
    "pycryptodomex"
]

VERSION = (0, 0, 1)
__version__ = '.'.join(map(str, VERSION))

setup(
    name="tornado_playground",
    version=__version__,
    description="My playground",
    author="Martin Dulin",
    author_email='martin@dulin.me.uk',
    keywords='web tornado',
    packages=find_packages(),
    install_requires=requires,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "serve = app:main",
        ],
    },
)
