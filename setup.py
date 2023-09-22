import os

from setuptools import find_packages, setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


version = "4.0.0"

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
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "Framework :: Zope2",
        "Framework :: Zope :: 4",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
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
            "plone.app.robotframework",
            "plone.dexterity",
            "Products.CMFCore",
            "requests",
        ]
    ),
    install_requires=[
        "setuptools",
        "collective.monkeypatcher",
        "zope.component",
        "zope.interface",
        "zope.publisher",
        "zope.traversing",
        "Products.CMFCore",
        "Zope2",
        "six",
    ],
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
