from distutils.core import setup

setup(
    name='lesstatic',
    version='0.6.0',
    author='Mike Zamansky',
    author_email='zamansky@gmail.com',
    packages=['lesstatic'],
    scripts=['bin/lesstatic'],
    url='http://github.com/zamansky/lesstatic',
    license='LICENSE.txt',
    description='LesStatic Static Site Generator',
    long_description=open('README.md').read(),
)
