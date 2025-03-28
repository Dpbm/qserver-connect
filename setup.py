from setuptools import setup, find_packages


def get_requirements():
    """
    Get requirements from 'requirements.txt'
    """
    with open("requirements.txt", "r", encoding="UTF-8") as file:
        lines = list(map(lambda line: line.replace("\n", "").strip(), file.readlines()))
        return lines


def get_long_description():
    """
    Fit readme.md into a string
    """

    with open("README.md", "r", encoding="UTF-8") as file:
        return file.read()


setup(
    name="qserver_connect",
    version="0.0.21",
    install_requires=get_requirements(),
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Quantum Computing",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: System",
        "Topic :: System :: Hardware",
    ],
    url="https://github.com/Dpbm/qserver-connect",
    license="MIT",
    author="Dpbm",
    author_email="dpbm136@gmail.com",
    description="A library to interact with your qserver",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
)
