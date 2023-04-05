from setuptools import setup, find_packages

setup(
	name='sagae',
	version='1.0',
	author='Sagar Singh',
	authour_email='sagar.singh-1@ou.edu',
	packages=find_packages(exclude=('tests', 'docs')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)
