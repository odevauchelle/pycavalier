from setuptools import setup, find_packages

setup(name="pycacalier",
      version="0.1",
      author="Olivier Devauchelle",
      license="GPL",
      long_description=__doc__,
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "numpy",
          "matplotlib",
      ])
