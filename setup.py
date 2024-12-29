from pathlib import Path
import setuptools

directory = Path(__file__).resolve().parent
with open(directory / 'README.md', encoding='utf-8') as f:
  long_description = f.read()

setuptools.setup(
    name="xiangqi",
    version="0.0.1",
    author="Hung Ba Huynh",
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.11",
    install_requires=[],
    extras_require={ "dev": ["pytest"] },
)