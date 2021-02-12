from setuptools import find_packages, setup

setup(
    name='testbandit',
    packages=find_packages( include=[ 'testbandit' ] ),
    version='0.1.0',
    description='Test Bandit: A Python Library for Bayesian A/B and Bandit Testing',
    author='Javid Jamae',
    license='MIT',
    install_requires=[ 'scipy', 'matplotlib' ],
    tests_require=['nose'],
    test_suite='tests',
)
