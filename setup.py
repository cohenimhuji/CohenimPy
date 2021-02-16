from setuptools import setup, find_packages

setup(
    name='CohenimPy',
    version='0.01',
    author='Cohen Nimrod',
    author_email='cohenim@gmail.com',
    description='Various insanely helpful functions',
    packages=find_packages(),
    install_requires=[
        'sympy',
        'scipy',
            'pathos',
            'matplotlib',
            'numpy',
            'numba'
    ],
)
