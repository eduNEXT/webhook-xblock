#!/usr/bin/env python
"""
Package metadata for webhook_xblock.
"""
import os
import re
import sys

from setuptools import find_packages, setup


def get_version(*file_paths):
    """
    Extract the version string from the file.

    Input:
     - file_paths: relative path fragments to file with
                   version string
    """
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.

    Returns:
        list: Requirements file relative path strings
    """
    requirements = set()
    for path in requirements_paths:
        requirements.update(
            line.split('#')[0].strip() for line in open(path).readlines()
            if is_requirement(line.strip())
        )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement.

    Returns:
        bool: True if the line is not blank, a comment, a URL, or
              an included file
    """
    return line and not line.startswith(('-r', '#', '-e', 'git+', '-c'))


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


VERSION = get_version('webhook_xblock', '__init__.py')

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (VERSION, VERSION))
    os.system("git push --tags")
    sys.exit()

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
CHANGELOG = open(os.path.join(os.path.dirname(__file__), 'CHANGELOG.rst')).read()

setup(
    name='webhook-xblock',
    version=VERSION,
    description="""An X-block to send a payload with basic information about the course and student to a configurable URL.""",
    long_description=README + '\n\n' + CHANGELOG,
    author='eduNEXT',
    author_email='technical@edunext.co',
    url='https://github.com/eduNEXT/webhook-xblock',
    packages=find_packages(
        include=['webhook_xblock', 'webhook_xblock.*'],
        exclude=["*tests"],
    ),
    include_package_data=True,
    install_requires=load_requirements('requirements/base.in'),
    python_requires=">=3.11",
    license="AGPL 3.0",
    zip_safe=False,
    keywords='Python edunext xblock webhook-xblock',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    entry_points={
        'xblock.v1': [
            'webhook-xblock = webhook_xblock:WebhookXblock',
        ],
        'lms.djangoapp': [
            "webhook_xblock = webhook_xblock.apps:WebhookXblockConfig",
        ],
        'cms.djangoapp': [
            "webhook_xblock = webhook_xblock.apps:WebhookXblockConfig",
        ],
    },
    package_data=package_data("webhook_xblock", ["static", "public"]),
)
