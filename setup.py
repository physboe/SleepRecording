import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ble-rr-logger-physboe",
    version="1.0.0",
    author="Andre Boeni",
    author_email="boeni10@gmail.com",
    description="A little tool to read RR intervalls from BLE Device and save it",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/physboe/BLEHeartRateRRLogger.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    python_requires='>=2.7',
)
