import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hanziPhon", # Replace with your own username
    version="0.0.1",
    author="Yongfu Liao",
    author_email="liao961120@gmail.com",
    description="Hanzi phonetic interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liao961120/hanziPhon",
    package_dir = {'': 'src'},
    packages=['hanziPhon'],
    package_data={
        "": ["data/*.txt", "data/*.json", "data/*.csv"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
