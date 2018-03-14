# https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


setup(
    options={
        'python_setup': {
            'executable': './venv/bin/python ./venv/bin/ipython',
        },
    },
    name='bus-driver',
    # package_dir = {'': 'src'},
    version='0.1.0',
    author='ernie',
    packages=find_packages(),
    # scripts=['bin/hello.py',],
    entry_points={ 'console_scripts': ['bp_dallas=scripts.dallas:main', 'bp_stlcd=scripts.st:main']},
    url='na',
    license='na',
    description='Useful towel-related stuff.',
    long_description=open('README.md').read(),
    install_requires=[
        "pyserial",
    ]
)
