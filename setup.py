from setuptools import setup, find_packages

setup(
    name='CohenimPy',
    version='0.0171',
    author='Cohen Nimrod',
    author_email='nimrod.cohen1@mail.huji.ac.il',
    description='Various insanely helpful functions',
    packages=find_packages(),
    install_requires=[
        'datetime',
        'IPython',
        'matplotlib',
        'numba',
        'numpy',
        #'os',        
        'pandas',
        'pathlib',
        'pathos',
        'scipy',
        'statsmodels',
        #'subprocess',
        'sympy',
        #'sys'        
    ],
)
