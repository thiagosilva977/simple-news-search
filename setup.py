from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

REQUIRED_PKGS = [
    'setuptools',
    'beautifulsoup4',
    'click',
    'lxml',
    'numpy<2',
    'pandas',
    'pyarrow',
    'requests',
    'spacy',
    'sentence-transformers',
    'openpyxl',
]
EXTRAS_REQUIRE = {
    "full": [
        "torchvision",
        'langchain'
    ]}

setup(
    name="news-data-extractor",
    version="0.0.1",
    author="Thiago Silva",
    author_email="",
    description="Extract news in different sources.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thiagosilva977/simple-news-search-engine",
    packages=find_packages(),
    classifiers=[],
    python_requires=">=3.11",
    install_requires=REQUIRED_PKGS,
    extras_require=EXTRAS_REQUIRE,
    include_package_data=True,
    zip_safe=False
)
