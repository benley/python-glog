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
        log.check(True)
        self.assertRaises(log.FailedCheckException, log.check, False)
        return
    
    def test_check_eq(self):
        log.check_eq(1, 1)
        self.assertRaises(log.FailedCheckException, log.check_eq, 1, 2)
        return
    
    def test_check_ne(self):
        log.check_ne(1, 2)
        self.assertRaises(log.FailedCheckException, log.check_ne, 1, 1)
        return
    
    def test_check_le(self):
        log.check_le(1, 2)
        log.check_le(1, 1)
        self.assertRaises(log.FailedCheckException, log.check_le, 1.1, 1)
        return
    
    def test_check_ge(self):
        log.check_ge(2, 1)
        log.check_ge(1, 1)
        self.assertRaises(log.FailedCheckException, log.check_ge, 1, 1.1)
        return
    
    def test_check_lt(self):
        log.check_lt(1, 2)
        self.assertRaises(log.FailedCheckException, log.check_lt, 1, 1)
        return
    
    def test_check_gt(self):
        log.check_gt(2, 1)
        self.assertRaises(log.FailedCheckException, log.check_gt, 1, 1)
        return
    
    def test_check_not_none(self):
        log.check_notnone('not none')
        self.assertRaises(log.FailedCheckException, log.check_notnone, None)
        return
     
 
if __name__ == '__main__':
    unittest.main()
