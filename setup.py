from setuptools import setup, find_packages

setup(
    name="openfiles-python",
    version="1.0.0",
    description="Python SDK for Openfiles API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Openfiles",
    author_email="info@openfiles.xyz",
    url="https://github.com/Gusarich/openfiles-python",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="openfiles, ton, storage, api, sdk",
)
