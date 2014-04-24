import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='python-cec-crawler',
    version='0.0.1',
    py_modules=['crawler'],
    license='MIT License',
    description='Crawler para busca de produtos no site do CEC',
    long_description=README,
    url='https://github.com/LucasMagnum/cec_crawler',
    author='Lucas Magnum Lopes Oliveira',
    author_email='contato@lucasmagnum.com.br',
)