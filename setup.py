#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script para o Sistema de Processamento CNAB 400 - Bradesco
"""

from setuptools import setup, find_packages
import os

# Ler o README para a descrição longa
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Ler os requisitos
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cnab-bradesco-processor",
    version="1.2.0",
    author="Sistema CNAB Bradesco",
    author_email="contato@exemplo.com",
    description="Sistema completo para processamento de arquivos CNAB 400 do Bradesco",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/cnab-bradesco",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "cnab-bradesco=iniciar:main",
            "cnab-gui=cnab_bradesco_gui:main",
            "cnab-lote=processar_lote:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.ico", "*.txt", "*.md"],
    },
    keywords="cnab bradesco banco processamento financeiro cobranca",
    project_urls={
        "Bug Reports": "https://github.com/seu-usuario/cnab-bradesco/issues",
        "Source": "https://github.com/seu-usuario/cnab-bradesco",
        "Documentation": "https://github.com/seu-usuario/cnab-bradesco/blob/main/docs/README.md",
        "Changelog": "https://github.com/seu-usuario/cnab-bradesco/blob/main/CHANGELOG.md",
    },
) 