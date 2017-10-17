from setuptools import setup, find_packages
from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

pfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pfile['packages'], r=False)

setup(
    name='fptools',
    version='0.1.0',
    description='Functional programming tools for Python',
    url='https://github.com/kang-health/fptools',
    author='Iddan Aharonson',
    author_email='iddan@kanghealth.io',
    install_requires=requirements,
    platforms="any"
)
