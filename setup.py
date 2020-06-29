import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

REQUIRE = []
with open("requirements.txt" "r") as f:
    requirements = f.readlines()
    REQUIRE = [r.strip() for r in requirements]


setuptools.setup(
    name="cloudLogQueryAndNotify",
    version="0.0.1",
    author="diepthuyhan",
    author_email="diepthuyhan",
    description="Query Log From Cloud Provider and Notify",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diepthuyhan/cloudQueryLogAndNotify",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=REQUIRE
)
