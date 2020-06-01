from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ble_rr_logger",
    version="1.0.0",
    author="Andre Boeni",
    author_email="boeni10@gmail.com",
    description="A little tool to read RR intervalls from BLE Device and " +
                "save it to a sqlite3 database. " +
                "You need gatttool to make it work.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/physboe/BLEHeartRateRRLogger.git",
    classifiers=[
        "Programming Language :: Python :: 3.7.3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux, Raspberry Pi",
    ],
    python_requires='>=3.7.3',
    packages=find_packages(),
    install_requires=['pexpect==4.8.0'],
)
