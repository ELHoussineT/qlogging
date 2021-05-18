from setuptools import setup, find_packages

__version__ = "1.0.5"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='qlogging',
    version=__version__,

    url='https://github.com/sinkingtitanic/qlogging',
    author='Sinking Titanic',
    author_email='ofcourse7878@gmail.com',
    description="Beautifully colored, quick and simple Python logging.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',

    packages=find_packages(),


    install_requires=[
    'colorama',
    ],
    py_modules=['qlogging'],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Logging",
        "Topic :: System :: Monitoring"
    ]
)