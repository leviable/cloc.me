import os
from setuptools import setup

modules = ['clocme', ]

setup(
    name="clocme",
    author='Levi Noecker',
    author_email='levi.noecker@gmail.com',
    url='https://github.com/levi-rs/cloc.me',
    description="Clocme controller",
    py_modules=modules,
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'clocme=cli:main',
        ]
    }
)
