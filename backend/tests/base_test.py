

import logging

import tornado.testing


class BaseTest(tornado.testing.AsyncTestCase):
  """ A testing base class. Right now, it just initializes logging. """

  def setUp(self):
    super().setUp()

    # Initialize logging.
    self.__root = logging.getLogger()
    self.__root.setLevel(logging.DEBUG)

    self.__stream_handler = logging.StreamHandler()
    self.__stream_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(name)s@%(asctime)s: " +
        "[%(levelname)s] %(message)s")
    self.__stream_handler.setFormatter(formatter)

    self.__root.addHandler(self.__stream_handler)

  def tearDown(self):
    super().tearDown()

    # Disable logging.
    self.__root.removeHandler(self.__stream_handler)
