import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
CHANGES = ''

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid_redis_sessions',
    'waitress',
    ]

setup(name='SocietyBuilder',
      version='0.0',
      description='Society Builder social platform',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='community',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="ist",
      entry_points="""\
      [paste.app_factory]
      main = ist:main
      """,
      )
