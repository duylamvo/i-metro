from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# all folder with __init__.py as packages
packages = find_packages(
    exclude=("tests*",)
)

setup(name="libopt",
      version="0.0.1",
      author="Duy Lam Vo",
      author_email="duy-lam.vo1102@outlook.com",
      description="libopt",
      long_description=long_description,
      url="https://github.com/duylamvo/i-metro",
    #   package_dir={'': 'libopt'},
      packages=packages,
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.6'

      )
