import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cdk_classic_app",
    version="0.0.1",
    description="ELB + ASG + EC2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="author",
    package_dir={"": "lib"},
    packages=setuptools.find_packages(where="cdk_classic_app"),
    install_requires=[
        "aws-cdk-lib==2.69.0",
        "constructs>=10.0.0,<11.0.0"
    ],
)