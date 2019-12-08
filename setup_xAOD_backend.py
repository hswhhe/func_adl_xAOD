# setuptools loads some plugins necessary for use here.
from setuptools import find_packages  # noqa: F401
from distutils.core import setup
from version_info import version_func_adl_xaod_backend

# Use the readme as the long description.
with open("README.md", "r") as fh:
    long_description = fh.read()

xaod_template_files = []
setup(name="func_adl_xAOD.backend",
      version=version_func_adl_xaod_backend,
      packages=['func_adl_xAOD.backend'] + [f'func_adl_xAOD.backend.{f}' for f in ['cpplib', 'dataset_resolvers', 'xAODlib']],
      scripts=[],
      description="Backend to generate and run C++ files for Functional Analysis Description Language for accessing ATLAS xAOD files.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="G. Watts (IRIS-HEP/UW Seattle)",
      author_email="gwatts@uw.edu",
      maintainer="Gordon Watts (IRIS-HEP/UW Seattle)",
      maintainer_email="gwatts@uw.edu",
      url="https://github.com/iris-hep/func_adl_xAOD",
      license="TBD",
      test_suite="tests",
      install_requires=[
          "requests~=2.0",
          "pandas~=0.24",
          "uproot~=3.7",
          "retry~=0.9",
          "func_adl==1.0.0a17",
      ],
      setup_requires=["pytest-runner"],
      tests_require=["pytest>=3.9", "pytest-cov"],
      classifiers=[
          "Development Status :: 3 - Alpha",
          # "Development Status :: 4 - Beta",
          # "Development Status :: 5 - Production/Stable",
          # "Development Status :: 6 - Mature",
          "Intended Audience :: Developers",
          "Intended Audience :: Information Technology",
          "Programming Language :: Python",
          "Topic :: Software Development",
          "Topic :: Utilities",
      ],
      data_files=[],
      platforms="Any",
      )