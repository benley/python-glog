glog
====

A simple Google-style logging wrapper for Python.

This library attempts to greatly simplify logging in Python
applications. Nobody wants to spend hours pouring over the PEP 282
logger documentation, and almost nobody actually needs things like
loggers that can be reconfigured over the network. We just want to get
on with writing our apps.

Styled somewhat after the twitter.common.log_ interface, which in turn was
modeled after Google's internal python logger, which was `never actually
released`_ to the wild, and which in turn was based on the `C++ glog module`_.

Core benefits
-------------

-  You and your code don't need to care about how logging works. Unless
   you want to, of course.

-  No more complicated setup boilerplate!

-  Your apps and scripts will all have a consistent log format, and the
   same predictable behaviours.

This library configures the root logger, so nearly everything you import
that uses the standard Python logging module will play along nicely.

Behaviours
----------

-  Messages are always written to stderr.

-  Lines are prefixed with a google-style log prefix, of the form

``E0924 22:19:15.123456 19552 filename.py:87] Log message blah blah``

Splitting on spaces, the fields are:

1. The first character is the log level, followed by MMDD (month, day)
2. HH:MM:SS.microseconds
3. Process ID
4. basename\_of\_sourcefile.py:linenumber]
5. The body of the log message.

Example use
-----------

.. code:: python

    import glog as log

    log.info("It works.")
    log.warn("Something not ideal")
    log.error("Something went wrong")
    log.fatal("AAAAAAAAAAAAAAA!")

If your app uses gflags_, it will automatically gain a --verbosity flag.
In order for that flag to be effective, you must call log.init() after
parsing flags, like so:

.. code:: python

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

Happy logging!

.. _twitter.common.log: https://github.com/twitter/commons/tree/master/src/python/twitter/common/log
.. _never actually released: https://groups.google.com/d/msg/google-glog/a_JcyJ4p8MQ/Xu-vDPiuCCYJ
.. _C++ glog module: https://github.com/google/glog
.. _gflags: https://github.com/google/python-gflags
