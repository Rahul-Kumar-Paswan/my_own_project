from setuptools import setup, find_packages

setup(
    name="python_demo",
    version='1.0.0',
    packages=find_packages(),
    description='A Simple Python Package',
    author='Rahul_Paswan',
    install_requires=[
        "Flask==2.0.1",
        "Flask-MySQLdb==1.0.1",
        "Werkzeug==2.0.2",
        "Jinja2==3.1.2",
        "MarkupSafe==2.1.3",
        "mysqlclient==2.2.0",
        "itsdangerous==2.1.2",
        "setuptools==68.2.2",
        "wheel==0.41.2"
    ],
)
