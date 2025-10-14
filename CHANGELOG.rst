Change Log
----------

..
   All enhancements and patches to webhook_xblock will be documented
   in this file.  It adheres to the structure of https://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).
   
   This project adheres to Semantic Versioning (https://semver.org/).

.. There should always be an "Unreleased" section for changes pending release.

Unreleased
~~~~~~~~~~

*

1.2.0 - 2025-10-14
**********************************************

Changed
=======

* **Ulmo Support**: Upgrade requirements base on edx-platform Ulmo release, update GitHub Workflows with new actions version.

1.1.0 - 2025-06-22
**********************************************

Changed
=======

* **Teak Support**: Upgrade requirements based on edx-platform Teak release, update GitHub Actions workflows to use the `ubuntu-22.04` runner image.

1.0.1 - 2025-02-04
**********************************************

Changed
=======

* **Replaced `pkg_resources` with `importlib.resources`**  
  - `pkg_resources` (from `setuptools`) is deprecated and may be removed in future Python versions.  
  - Now using `importlib.resources`, the recommended alternative for managing package resources.  
  - This improves performance and ensures better compatibility with modern Python versions.  


[1.0.0] - 2025-01-19
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Support for python 3.11 and Django 4.2.
* Unit and quality tests.

Removed
_____

* Support for Python <3.11 and Django <4.2


[0.1.0] - 2021-07-13
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* First release on PyPI.
