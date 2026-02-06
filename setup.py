"""
Setup script for Greene County Property Finder

This allows the project to be installed as a package:
    pip install -e .
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
if requirements_path.exists():
    requirements = [
        line.strip() 
        for line in requirements_path.read_text().splitlines() 
        if line.strip() and not line.startswith("#")
    ]
else:
    requirements = [
        "streamlit>=1.31.0",
        "pandas>=2.0.0",
        "folium>=0.15.0",
        "streamlit-folium>=0.18.0",
        "requests>=2.31.0",
    ]

setup(
    name="greene-county-property-finder",
    version="1.0.0",
    author="Victor K Jung",
    author_email="",
    description="OnXHunt-style property identification for Greene County, NY",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/victorkjung/NYS-Greene-County-Property-Search",
    project_urls={
        "Bug Tracker": "https://github.com/victorkjung/NYS-Greene-County-Property-Search/issues",
        "Documentation": "https://github.com/victorkjung/NYS-Greene-County-Property-Search#readme",
        "Source Code": "https://github.com/victorkjung/NYS-Greene-County-Property-Search",
    },
    packages=find_packages(exclude=["tests", "tests.*", "docs"]),
    py_modules=[
        "app",
        "greene_county_fetcher",
        "data_loader",
        "nys_data_fetcher",
        "constants",
        "ui",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fetch-parcels=greene_county_fetcher:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Streamlit",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    keywords=[
        "streamlit",
        "property",
        "real-estate",
        "gis",
        "mapping",
        "greene-county",
        "catskills",
        "new-york",
        "parcels",
    ],
    include_package_data=True,
    package_data={
        "": ["*.toml", "*.yaml", "*.yml", "*.md"],
    },
    zip_safe=False,
)
