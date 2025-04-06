#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# python3 prg_general_config_and_state_test.py

import unittest
import prg_general_config_and_state

class TestPrgNew(unittest.TestCase):

    def test_root_dir_detected(self):
        prg = prg_general_config_and_state.Prg()

        self.assertTrue(prg.initErrors == list() )
        dirRootDetected, _errors = prg.get("deepcopy_dir_root")
        self.assertTrue(dirRootDetected.endswith("deepcopy"))

        osDetected, _errors = prg.get("operation_system")
        self.assertTrue(osDetected in ["Linux", "Windows", "Darwin"])


if __name__ == '__main__':
    unittest.main()
