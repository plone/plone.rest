from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


version = "5.0.1.dev0"

long_description = read("README.rst") + "\n\n" + read("CHANGES.rst") + "\n\n"


setup(
    name="plone.rest",
    version=version,
    description="Plone support for HTTP verbs.",
    long_description=long_description,
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "Framework :: Plone :: Core",
        "Framework :: Zope2",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="rest http",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://github.com/plone/plone.rest/",
    license="GPL version 2",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["plone"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    extras_require=dict(
        test=[
            "plone.app.testing[robot]>=4.2.2",
            "requests",
            "BTrees",
            "plone.app.contenttypes[test]",
            "plone.app.redirector",
            "plone.app.textfield",
            "plone.namedfile",
            "plone.testing",
            "z3c.relationfield",
            "zope.intid",
        ]
    ),
    install_requires=[
        "setuptools",
        "collective.monkeypatcher",
        "Products.CMFCore",
        "Zope",
        "plone.memoize",
        "zope.browserpage",
    ],
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
