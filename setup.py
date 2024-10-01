from setuptools import setup, find_packages

setup(
    name="monday-api",
    version="0.1",
    description="A Python client for the Monday.com API",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Enzo Garofalo",
    author_email="egarofalo@salas.plus",
    url="https://github.com/egarofalo-salasplus/monday_api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
