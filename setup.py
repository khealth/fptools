from setuptools import setup

setup(
    name='fptools',
    version='0.2.1',
    description='Functional programming tools for Python',
    url='https://github.com/kang-health/fptools',
    author='Iddan Aharonson',
    author_email='iddan@kanghealth.io',
    packages=['fptools'],
    install_requires=[
        'cardinality',
    ],
    platforms="any",
)
