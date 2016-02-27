"""A simple Google-style logging wrapper.

This library attempts to greatly simplify logging in Python applications.
Nobody wants to spend hours pouring over the PEP 282 logger documentation, and
almost nobody actually needs things like loggers that can be reconfigured over
the network.  We just want to get on with writing our apps.

## Core benefits

* You and your code don't need to care about how logging works. Unless you want
  to, of course.

* No more complicated setup boilerplate!

* Your apps and scripts will all have a consistent log format, and the same
  predictable behaviours.

This library configures the root logger, so nearly everything you import
that uses the standard Python logging module will play along nicely.

## Behaviours

* Messages are always written to stderr.

* Lines are prefixed with a google-style log prefix, of the form

      E0924 22:19:15.123456 19552 filename.py:87] Log message blah blah

  Splitting on spaces, the fields are:

    1. The first character is the log level, followed by MMDD (month, day)
    2. HH:MM:SS.microseconds
    3. Process ID
    4. basename_of_sourcefile.py:linenumber]
    5. The body of the log message.


## Example logging usage

    import glog as log

    log.info("It works.")
    log.warn("Something not ideal")
    log.error("Something went wrong")
    log.fatal("AAAAAAAAAAAAAAA!")

If your app uses gflags, it will automatically gain a --verbosity flag. In
order for that flag to be effective, you must call log.init() after parsing
flags, like so:

    import sys
    import gflags
    import glog as log

    FLAGS = gflags.FLAGS

    def main():
      log.debug('warble garble %s', FLAGS.verbosity)

    if __name__ == '__main__':
        posargs = FLAGS(sys.argv)
        log.init()
        main(posargs[1:])

## Example check usage

The C++ glog library provides a set of macros that help document and enforce
invariants.  These are superior to standard python asserts because they provide
a message indicating the values that caused the check to fail.  This helps in
reproducing failure cases and provides values for test cases.

https://google-glog.googlecode.com/svn/trunk/doc/glog.html#check


    import glog as log
    import math
    
    def compute_something(a):
        log.check_eq(type(a), float) # require floating point types
        log.check_ge(a, 0) # require non-negative values
        value = math.sqrt(a)
        return value
   
    if __name__ == '__main__':
        compute_something(10)

Happy logging!
"""

import logging
import time
import traceback
import os
import sys
import gflags

gflags.DEFINE_integer('verbosity', logging.INFO, 'Logging verbosity.',
                      short_name='v')
FLAGS = gflags.FLAGS


def format_message(record):
    try:
        record_message = '%s' % (record.msg % record.args)
    except TypeError:
        record_message = record.msg
    return record_message


class GlogFormatter(logging.Formatter):
    LEVEL_MAP = {
        logging.FATAL: 'F',  # FATAL is alias of CRITICAL
        logging.ERROR: 'E',
        logging.WARN: 'W',
        logging.INFO: 'I',
        logging.DEBUG: 'D'
    }

    def __init__(self):
        logging.Formatter.__init__(self)

    def format(self, record):
        try:
            level = GlogFormatter.LEVEL_MAP[record.levelno]
        except:
            level = '?'
        date = time.localtime(record.created)
        date_usec = (record.created - int(record.created)) * 1e6
        record_message = '%c%02d%02d %02d:%02d:%02d.%06d %s %s:%d] %s' % (
            level, date.tm_mon, date.tm_mday, date.tm_hour, date.tm_min,
            date.tm_sec, date_usec,
            record.process if record.process is not None else '?????',
            record.filename,
            record.lineno,
            format_message(record))
        record.getMessage = lambda: record_message
        return logging.Formatter.format(self, record)

logger = logging.getLogger()
handler = logging.StreamHandler()

level = logger.level


def setLevel(newlevel):
    logger.setLevel(newlevel)
    FLAGS.verbosity = newlevel
    logger.debug('Log level set to %s', newlevel)


def init():
    setLevel(FLAGS.verbosity)

debug = logging.debug
info = logging.info
warning = logging.warning
warn = logging.warning
error = logging.error
exception = logging.exception
fatal = logging.fatal
log = logging.log

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
WARN = logging.WARN
ERROR = logging.ERROR
FATAL = logging.FATAL

_level_names = {
    DEBUG: 'DEBUG',
    INFO: 'INFO',
    WARN: 'WARN',
    ERROR: 'ERROR',
    FATAL: 'FATAL'
}

_level_letters = [name[0] for name in _level_names.values()]

GLOG_PREFIX_REGEX = (
    r"""
    (?x) ^
    (?P<severity>[%s])
    (?P<month>\d\d)(?P<day>\d\d)\s
    (?P<hour>\d\d):(?P<minute>\d\d):(?P<second>\d\d)
    \.(?P<microsecond>\d{6})\s+
    (?P<process_id>-?\d+)\s
    (?P<filename>[a-zA-Z<_][\w._<>-]+):(?P<line>\d+)
    \]\s
    """) % ''.join(_level_letters)
"""Regex you can use to parse glog line prefixes."""

handler.setFormatter(GlogFormatter())
logger.addHandler(handler)
setLevel(FLAGS.verbosity)


# Define functions emulating C++ glog check-macros 
# https://google-glog.googlecode.com/svn/trunk/doc/glog.html#check

def format_stacktrace(stack):
    """ Print a stack trace that is easier to read. 
    * Reduce paths to basename component
    * Truncates the part of the stack after the check failure
    """
    lines = []
    for i, f in enumerate(stack):
        name = os.path.basename(f[0])
        line = "\t%s:%d\t%s" % (name + "::" + f[2], f[1], f[3])
        lines.append(line)    
    return lines


class FailedCheckException(Exception):

    """ Exception with message indicating check-failure location and values. """

    def __init__(self, message):
        self.message = message
        return

    def __str__(self):
        return self.message


def check_failed(message):
    stack = traceback.extract_stack()
    stack = stack[0:-2]
    stacktrace_lines = format_stacktrace(stack)
    process = os.getpid()
    filename, line_num, _, _ = stack[-1]
    created = time.time()
    date = time.localtime(created)
    date_usec = (created - int(created)) * 1e6
    try:
        raise FailedCheckException(message)
    except FailedCheckException:
        log_record = logger.makeRecord('CRITICAL', 50, filename, line_num, message, None, None)
        handler.handle(log_record)    
        
        log_record = logger.makeRecord('DEBUG', 10, filename, line_num, 'Check failed here:' , None, None)
        handler.handle(log_record)
        for line in stacktrace_lines:
            log_record = logger.makeRecord('DEBUG', 10, filename, line_num, line, None, None)
            handler.handle(log_record)
        raise
    return
    
def check(condition, message=None):
    """ Raise exception with message if condition is False """
    if not condition:
        if message is None:
            message = "Check failed."
        check_failed(message)


def check_eq(obj1, obj2, message=None):
    """ Raise exception with message if obj1 != obj2. """
    if obj1 != obj2:
        if message is None:
            message = "check failed: %s != %s" % (str(obj1), str(obj2))
        check_failed(message)


def check_ne(obj1, obj2, message=None):
    """ Raise exception with message if obj1 == obj2. """
    if obj1 == obj2:
        if message is None:
            message = "check failed: %s == %s" % (str(obj1), str(obj2))
        check_failed(message)


def check_le(obj1, obj2, message=None):
    """ Raise exception with message if not (obj1 <= obj2). """
    if obj1 > obj2:
        if message is None:
            message = "check failed: %s > %s" % (str(obj1), str(obj2))
        check_failed(message)


def check_ge(obj1, obj2, message=None):
    """ Raise exception with message if not (obj1 >= obj2)
    """
    if obj1 < obj2:
        if message is None:
            message = "check failed: %s < %s" % (str(obj1), str(obj2))
        check_failed(message)


def check_lt(obj1, obj2, message=None):
    """ Raise exception with message if not (obj1 < obj2). """
    if obj1 >= obj2:
        if message is None:
            message = "check failed: %s >= %s" % (str(obj1), str(obj2))
        check_failed(message)


def check_gt(obj1, obj2, message=None):
    """ Raise exception with message if not (obj1 > obj2). """
    if obj1 <= obj2:
        if message is None:
            message = "check failed: %s <= %s" % (str(obj1), str(obj2))
        check_failed(message)


def check_notnone(obj, message=None):
    """ Raise exception with message if obj is None """
    if obj is None:
        if message is None:
            message = "Check failed. Object is None."
        check_failed(message)



