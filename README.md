# BLEHeartRateRRLogger

This is a simple tool to read R-R Interval from BLE Device and store it in a SQLite Database. To make it work you will need to install gatttool on your machine. It's only tested with an SUUNTO-Smart heart belt sensor.

## Usage
This tool can be used from a terminal or as a module in your source code

### Terminal Usage
```sh
python -m blehrmlogger [args]
```

There is a help function
```sh
python -m blehrmlogger --help
```
### Code Usage
```python
databaselayer = dbl.DatabaseLayer("database.data")
gatttoolutil = ble.BLEHearRateService("gatttool", false)
gatttoolutil.connectToDevice("[you device mac]", "public")
gatttoolutil.registeringToHrHandle()
gatttoolutil.startRecording(databaselayer)
gatttoolutil.close()
```
