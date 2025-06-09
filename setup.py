from setuptools import setup, find_packages

setup(
    name="inmemory_fs",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.1.7",
        "dataclasses>=0.6",
    ],
    python_requires=">=3.9",
    entry_points={
        'console_scripts': [
            'fs=cli.filesys:main',
            'perms=cli.permissions:main',
        ],
    },
) 