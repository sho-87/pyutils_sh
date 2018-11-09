from setuptools import setup, find_packages
from distutils.util import convert_path


def readme():
    with open("README.rst") as f:
        return f.read()


meta = {}
with open(convert_path("pyutils_sh/version.py")) as f:
    exec(f.read(), meta)

setup(
    name="pyutils_sh",
    version=meta["__version__"],
    description="Assortment of Python utilities for my personal projects",
    long_description=readme(),
    url="https://github.com/sho-87/pyutils_sh",
    author="Simon Ho",
    author_email="simonho213@gmail.com",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3",
    install_requires=["numpy", "pandas", "matplotlib"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
    keywords="python utilities survey exam gaze spss data research statistics",
    zip_safe=True,
)
