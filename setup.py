"Setup script for the hostedpi package"

import sys
from setuptools import setup, find_packages

if not sys.version_info >= (3, 6):
    raise RuntimeError('This application requires Python 3.6 or later')

__project__ = 'hostedpi'
__version__ = '0.1'
__description__ = "Pythonic interface to the Mythic Beasts Hosted Pi API"
__python_requires__ = '>=3.6'
__author__ = 'Ben Nuttall'
__author_email__ = 'ben@bennuttall.com'
__url__ = 'https://bennuttall.com/'
__platforms__ = 'ALL'

__requires__ = ['requests']

__extra_requires__ = {}

__classifiers__ = [
    'Development Status :: 4 - Beta',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Utilities',
]

__entry_points__ = {
    'console_scripts': [
        'hostedpi = hostedpi.cli:main',
    ]
}



def main():
    "Executes setup when this script is the top-level"
    from pathlib import Path

    with Path(__file__).with_name('description.rst').open() as description:
        setup(
            name=__project__,
            version=__version__,
            description=__description__,
            long_description=description.read(),
            python_requires=__python_requires__,
            classifiers=__classifiers__,
            author=__author__,
            author_email=__author_email__,
            url=__url__,
            # license=[
            #     c.rsplit('::', 1)[1].strip()
            #     for c in __classifiers__
            #     if c.startswith('License ::')
            # ][0],
            # keywords=__keywords__,
            packages=find_packages(),
            include_package_data=True,
            platforms=__platforms__,
            install_requires=__requires__,
            extras_require=__extra_requires__,
            entry_points=__entry_points__,
        )


if __name__ == '__main__':
    main()
