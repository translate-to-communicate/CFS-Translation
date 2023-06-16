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
    python_requires=">=3.10",
)
