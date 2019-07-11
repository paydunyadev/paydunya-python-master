from setuptools import setup, Command
from unittest import TextTestRunner, TestLoader
from glob import glob
from os.path import splitext, basename, join as pjoin
try:
    from os.path import walk
except ImportError:
    from os import walk
import os


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        '''
        Finds all the tests modules in tests/, and runs them.
        '''
        testfiles = []
        for t in glob(pjoin(self._dir, 'tests', '*.py')):
            if not t.endswith('__init__.py'):
                testfiles.append('.'.join(
                    ['tests', splitext(basename(t))[0]])
                )
        import sys
        ROOT = os.path.dirname(os.getcwd())
        PAYDUNYA_LIBS = os.path.join(ROOT, "paydunya")
        sys.path.append(PAYDUNYA_LIBS)
        tests = TestLoader().loadTestsFromNames(testfiles)
        t = TextTestRunner(verbosity=1)
        t.run(tests)


class CleanCommand(Command):
    """Recursively Delete all compile python modules"""
    user_options = []

    def initialize_options(self):
        self._clean_me = []
        for root, dirs, files in os.walk('.'):
            for f in files:
                if f.endswith('.pyc'):
                    self._clean_me.append(pjoin(root, f))

    def finalize_options(self):
        pass

    def run(self):
        for clean_me in self._clean_me:
            try:
                os.unlink(clean_me)
            except:
                pass


def readme(filename='README.rst'):
    with open('README.rst') as f:
        text = f.read()
    f.close()
    return text

setup(
    name='paydunya',
    version=__import__('paydunya').__version__,
    author='PAYDUNYA',
    author_email='paydunya@paydunya.com',
    packages=['paydunya'],
    cmdclass={'test': TestCommand, 'clean': CleanCommand},
    scripts=[],
    url='https://github.com/paydunya/paydunya-python',
    license='LICENSE.txt',
    keywords="paydunya mobile money payments",
    description='PAYDUNYA Python client library',
    long_description=readme('README.rst'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=['requests >=2.0'],
)
