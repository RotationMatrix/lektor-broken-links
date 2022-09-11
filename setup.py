import ast
import io
import re

from setuptools import setup, find_packages

with io.open('README.md', 'rt', encoding="utf8") as f:
    readme = f.read()

_description_re = re.compile(r'description\s+=\s+(?P<description>.*)')

with open('lektor_broken_links.py', 'rb') as f:
    description = str(ast.literal_eval(_description_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    author='RotationMatrix',
    description=description,
    keywords='Lektor broken links plugin',
    license='MIT-License',
    long_description=readme,
    long_description_content_type='text/markdown',
    name='lektor-broken-links',
    packages=find_packages(),
    py_modules=['lektor_broken_links'],
    url='https://github.com/RotationMatrix/lektor-broken-links',
    version='0.1.2',
    classifiers=[
        'Framework :: Lektor',
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking',
    ],
    entry_points={
        'lektor.plugins': [
            'broken-links = lektor_broken_links:BrokenLinksPlugin',
        ]
    },
    install_requires=['mistune>=0.7.0,<2', 'click>=7.0', 'furl>=2.1.0']
)
