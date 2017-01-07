#!/usr/bin/python3

import logging
import os
import sys
import unittest


""" Runs all unit tests. """


def init_logging():
  """ Initializes logging for testing, just printing it to the screen. """
  # Configure root logger.
  root = logging.getLogger()
  root.setLevel(logging.DEBUG)

  stream_handler = logging.StreamHandler()
  stream_handler.setLevel(logging.DEBUG)

  formatter = logging.Formatter("%(name)s@%(asctime)s: " +
      "[%(levelname)s] %(message)s")
  stream_handler.setFormatter(formatter)

  root.addHandler(stream_handler)

def main():
  init_logging()
  logging.info("Starting tests...")

  loader = unittest.TestLoader()
  suite = loader.discover("tests", top_level_dir=os.getcwd())

  test_result = unittest.TextTestRunner(verbosity=2).run(suite)
  if not test_result.wasSuccessful():
    logging.critical("Unit tests failed.")
    return 1

  return 0


if __name__ == "__main__":
  sys.exit(main())
