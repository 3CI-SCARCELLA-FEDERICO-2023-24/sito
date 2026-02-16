"""
Script di setup per l'applicazione di riconoscimento facciale.
"""

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="face-recognition-app",
    version="1.0.0",
    description="Sistema di riconoscimento facciale con PyQt6",
    author="Sistema di Riconoscimento Facciale",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.10",
    entry_points={
        'console_scripts': [
            'face-recognition=main:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Video :: Capture",
    ],
)
