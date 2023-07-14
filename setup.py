from setuptools import find_packages, setup

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="CFS",
    version="0.0.1",
    description="An automated script to pull in calls-for-service (CFS) data and produce a "
                "single document meant for archiving and future analysis",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Christopher Romeo",
    author_email="caromeo@albany.edu",
    classifiers=[
        "Programming Language :: Python 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["pandas >= 2.0.2", "tabulate >= 0.9.0", "numpy >= 1.24.3", "sodapy >= 2.2.0",
                      "easygui >= 0.98.3", "geopy >= 2.3.0", "requests >= 2.31.0", "openpyxl >= 3.1.2"],
    python_requires=">=3.9.0",
)
