from setuptools import setup, find_packages
from copy import copy


requirements = [
    "numpy",
    "scipy",
    "matplotlib",
    "pyuvdata",
    "uvtools @ git+git://github.com/HERA-Team/uvtools",
]

test_requirements = copy(requirements)

setup(
    author="Tyler Cox",
    author_email="tyler.a.cox@berkeley.edu",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Python scripts for generating images and movies from radio interferomtry data",
    entry_points={"console_scripts": ["casa_imaging=casa_imaging.cli:main",],},
    install_requires=requirements,
    license="BSD license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="nucal",
    name="nucal",
    packages=find_packages(include=["casa_imaging", "casa_imaging.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/tyler-a-cox/HERA_beam_mapping",
    version="0.1.0",
    zip_safe=False,
)
