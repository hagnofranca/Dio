from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="lvl2equation",
    version="0.0.1",
    author="Hagno França",
    author_email="hagno.franca@icloud.com",
    description="Functins second degree equation",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.12',
)