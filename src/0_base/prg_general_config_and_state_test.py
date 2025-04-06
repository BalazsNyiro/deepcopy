#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# python3 prg_general_config_and_state_test.py

import unittest
import prg_general_config_and_state

class TestPrgNew(unittest.TestCase):

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
