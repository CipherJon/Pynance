from setuptools import find_packages, setup

setup(
    name="pynance",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["setuptools==68.2.2", "python-dateutil>=2.8.2"],
    entry_points={
        "console_scripts": [
            "calculator=calculator.main:main",
            "file-organizer=file_organizer.file_organizer.main:main",
            "pynance=pynance:main",
        ],
    },
)
