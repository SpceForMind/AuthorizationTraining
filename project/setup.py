from setuptools import setup

setup(
    name = "AuthTraining",
    packages = ["project"],
    include_package_data = True,
    install_requires = [
        "Flask==1.1.1",
        "SQLAlchemy==2.4.0",
        "Flask-Script==2.0.6",
        "Flask-WTF==0.14.2",
        "Flask-Migrate==2.5.2",
        "rauth==0.7.3",
        "Werkzeug==0.15.5",
        "WTForms==2.2.1"
    ]
)