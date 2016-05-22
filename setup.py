import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0a6'

long_description = (
    read('README.rst') + '\n\n' +
    read('CHANGES.rst') + '\n\n'
    )


setup(name='plone.rest',
      version=version,
      description="Plone support for HTTP verbs.",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
      ],
      keywords='',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.rest',
      license='GPL version 2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
          test=[
              'plone.app.testing[robot]>=4.2.2',
              'plone.app.robotframework',
              'plone.dexterity',
              'requests',
          ]
      ),
      install_requires=[
          'setuptools',
          'collective.monkeypatcher',
          'zope.component',
          'zope.interface',
          'zope.publisher',
          'zope.traversing',
          'Products.CMFCore',
          'Zope2',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
