import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cdk_network",
    version="0.0.1",
    description="Networking vpc + 4 subnets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="author",
    package_dir={"": "lib"},
    packages=setuptools.find_packages(where="cdk_network"),
    install_requires=[
        "aws-cdk-lib==2.69.0",
        "constructs>=10.0.0,<11.0.0"
    ],
)