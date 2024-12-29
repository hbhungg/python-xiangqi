import setuptools

setuptools.setup(
    name="xiangqi",
    version="0.0.1",
    packages=setuptools.find_packages(),
    python_requires=">=3.11",
    extras_require={ "dev": ["pytest"] },
)