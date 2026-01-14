from setuptools import find_packages, setup

setup(
    name="pynance",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "setuptools==68.2.2",
        "python-dateutil>=2.8.2",
        "nltk==3.8.1",
        "scikit-learn==1.4.0",
        "bcrypt==4.1.2",
        "Flask==3.0.2",
        "Flask-Login==0.6.2",
        "Flask-SQLAlchemy>=3.1.1",
        "SQLAlchemy>=2.0.28",
        "Flask-WTF==1.2.1",
        "Werkzeug==3.0.2",
        "python-dotenv==1.0.0",
        "markupsafe>=2.1.5",
        "Flask-Migrate",
        "Flask-CORS==5.0.1",
    ],
    entry_points={
        "console_scripts": [
            "calculator=calculator.main:main",
            "file-organizer=file_organizer.file_organizer.main:main",
            "pynance=pynance:main",
            "pybot=pybot.__init__:run_chatbot",
        ],
    },
)
