"""
Setup script for AgriTrade Pro application.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="agritrade-pro",
    version="1.0.0",
    author="AgriTrade Pro Development Team",
    author_email="contact@agritrade-pro.com",
    description="A multilingual AI assistant for agricultural market vendors in India",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/agritrade-pro",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Natural Language :: Hindi",
        "Natural Language :: Tamil",
        "Natural Language :: Telugu",
        "Natural Language :: Bengali",
        "Natural Language :: Marathi",
        "Natural Language :: Gujarati",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
            "mypy>=1.0",
            "pre-commit>=2.20.0",
        ],
        "test": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "hypothesis>=6.88.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agritrade-pro=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "mandi_setu": [
            "theme/*.css",
            "ui/templates/*.html",
            "data/*.sql",
        ],
    },
    keywords=[
        "agriculture",
        "trading",
        "multilingual", 
        "ai",
        "voice-interface",
        "india",
        "farmers",
        "market",
        "streamlit",
        "viksit-bharat"
    ],
    project_urls={
        "Bug Reports": "https://github.com/your-username/agritrade-pro/issues",
        "Source": "https://github.com/your-username/agritrade-pro",
        "Documentation": "https://github.com/your-username/agritrade-pro#readme",
        "Changelog": "https://github.com/your-username/agritrade-pro/blob/main/CHANGELOG.md",
    },
)