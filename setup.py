from distutils.core import  setup
from setuptools import find_packages

setup(
    name='Amico',
    version='1.0.0',
    url='https://github.com/01ly/Amico',
    description='A micro asynchronous Python website crawler framework',
    # long_description=open('README.md').read(),
    author='linkin',
    maintainer='linkin',
    maintainer_email='yooleak@outlook.com ',
    license='MIT',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['amico = amico.cmd:run']
    },
    install_requires=[
            'lxml',
            'bs4',
            'six>=1.5.2',
            'bloompy>=0.1.1',
        ],
    classifiers=[
        'Framework :: Amico',
        'Environment :: Console',
        'Intended Audience :: Python Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.5',
)