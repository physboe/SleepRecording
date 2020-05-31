import unittest
import blehrmlogger.ConfigLoader as configloader
import os


class TestConfigLoader(unittest.TestCase):

    def test_goodcase(self):
        try:
            confpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "/configs/WellTest.conf")
            configloader.loadConfigParameter(confpath)
        except KeyError:
            self.fail("Config File not Found")
        except Exception:
            self.fail("Thrown an Exception")
