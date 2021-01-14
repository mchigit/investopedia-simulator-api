from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Investopedia simulator trading API"
LONG_DESCRIPTION = (
    "An API that allows trading with stock simulator for from Investopedia"
)

install_requires = [
    'seleniumUtil'
]

setup(
    name="simulatorTradingApi",
    version=VERSION,
    author="Michael Chi",
    author_email="dychi1997@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    include_package_data=True,
)
