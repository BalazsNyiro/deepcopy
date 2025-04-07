#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# python3 prg_general_config_and_state_test.py

import unittest, platform
import prg_general_config_and_state

from unittest.mock import Mock
from unittest.mock import patch

class TestPrgNew(unittest.TestCase):

    def test_incorrect_python_major_version(self):

        # the mock is living only in this code section
        with patch("platform.python_version") as mock_python_version:
            #platform.python_version = Mock()  # https://realpython.com/python-mock-library/
            mock_python_version.return_value = "2.12.3"

            prg = prg_general_config_and_state.Prg()
            pythonMajor, errors = prg.get("python_interpreter_version_major")
            print(f"Test, Python interperter, major version: {pythonMajor}")
            self.assertTrue(pythonMajor < 3)
            self.assertTrue(len(prg.initErrors) > 0)


    def test_incorrect_python_minor_version(self):

        with patch("platform.python_version") as mock_python_version:
            mock_python_version.return_value = "2.11.3"

            prg = prg_general_config_and_state.Prg()
            pythonMinor, errors = prg.get("python_interpreter_version_minor")
            self.assertTrue(pythonMinor == 11)
            # print("initErrors:", prg.initErrors)
            self.assertTrue(len(prg.initErrors) > 0)
            self.assertIn("low version", str(prg.initErrors))
            



    def test_root_dir_detected(self):
        prg = prg_general_config_and_state.Prg()

        self.assertTrue(prg.initErrors == list() )
        dirRootDetected, errors = prg.get("deepcopy_dir_root")
        self.assertTrue(dirRootDetected.endswith("deepcopy"))
        self.assertTrue(len(errors)==0)

        osDetected, errors = prg.get("operation_system")
        self.assertTrue(osDetected in ["Linux", "Windows", "Darwin"])
        self.assertTrue(len(errors)==0)
        self.assertTrue(len(errors)==0)

        history, _err = prg.get_history("operation_system")
        self.assertTrue(len(history)>0)




if __name__ == '__main__':
    unittest.main()
