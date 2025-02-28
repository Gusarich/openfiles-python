from setuptools import setup, find_packages

setup(
    name="openfiles-python",
    version="1.0.0",
    description="Python SDK for Openfiles API",
    author="Openfiles",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0",
    ],
    python_requires=">=3.7",
)
