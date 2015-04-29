from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='pixhostuploader',
    version='1.0.9',
    description='Unofficial uploader to pixhost.org image sharing site.',
    long_description=readme(),
    url='https://github.com/martinsik/pixhost-uploader',
    author='Martin Sikora',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Utilities',
    ],
    install_requires=[
        'requests',
        'lxml'
    ],
    test_suite='tests',
)