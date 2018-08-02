from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='decomplexator',
    version='0.1',
    author='Jarek Zgoda',
    author_email='jaroslaw.zgoda@mobica.com',
    description='Python code complexity analyzer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zgoda-mobica/decomplexator',
    packages=find_packages(exclude=['docs', 'tests']),
    keywords='code complexity cyclomatic cognitive',
    install_requires=[
        'redbaron',
        'mccabe',
        'xdg',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-mock',
    ],
    entry_points={
        'console_scripts': [
            'cog=cog.run:main'
        ]
    },
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Quality Assurance',
    ),
    zip_safe=False,
    python_requires='~=3.5'
)
