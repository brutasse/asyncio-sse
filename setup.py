from setuptools import setup, find_packages

import sys

install_requires = ['aiohttp']
if sys.version_info < (3, 4):
    install_requires.append('asyncio')

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='asyncio-sse',
    version='0.1',
    author='Bruno Renié',
    author_email='bruno@renie.fr',
    url='https://github.com/brutasse/asyncio-sse',
    license='BSD',
    description='asyncio Server-Sent Events implementation',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    zip_safe=False,
)
