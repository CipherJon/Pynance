from setuptools import setup, find_packages

setup(
    name='calculator',
    version='0.1',
    packages=find_packages(),
    install_requires=["setuptools==68.2.2"],
    entry_points={
        'console_scripts': [
            'calculator=calculator.main:main',
        ],
    },
)