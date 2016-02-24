#!/usr/bin/python

import glog as log
import unittest

class TestLoggingMethods(unittest.TestCase):

    def test_debug(self):
        log.debug('test')
        return

    def test_info(self):
        log.info('test')
        return
    
    def test_warning(self):
        log.warning('test')
        return
    
    def test_warn(self):
        log.warn('test')
        return
    
    def test_error(self):
        log.error('test')
        return
    
    def test_fatal(self):
        log.fatal('test')
        return
 
 
class TestCheckMethods(unittest.TestCase):
    
    def test_check(self):
        log.CHECK(True)
        self.assertRaises(log.FailedCheckException, log.CHECK, False)
        return
    
    def test_check_eq(self):
        log.CHECK_EQ(1, 1)
        self.assertRaises(log.FailedCheckException, log.CHECK_EQ, 1, 2)
        return
    
    def test_check_ne(self):
        log.CHECK_NE(1, 2)
        self.assertRaises(log.FailedCheckException, log.CHECK_NE, 1, 1)
        return
    
    def test_check_le(self):
        log.CHECK_LE(1, 2)
        log.CHECK_LE(1, 1)
        self.assertRaises(log.FailedCheckException, log.CHECK_LE, 1.1, 1)
        return
    
    def test_check_ge(self):
        log.CHECK_GE(2, 1)
        log.CHECK_GE(1, 1)
        self.assertRaises(log.FailedCheckException, log.CHECK_GE, 1, 1.1)
        return
    
    def test_check_lt(self):
        log.CHECK_LT(1, 2)
        self.assertRaises(log.FailedCheckException, log.CHECK_LT, 1, 1)
        return
    
    def test_check_gt(self):
        log.CHECK_GT(2, 1)
        self.assertRaises(log.FailedCheckException, log.CHECK_GT, 1, 1)
        return
    
    def test_check_not_none(self):
        log.CHECK_NOTNONE('not none')
        self.assertRaises(log.FailedCheckException, log.CHECK_NOTNONE, None)
        return
     
 
if __name__ == '__main__':
    unittest.main()
