import logging

import tornado.testing

from .. import server


class _BaseTestMixin:
  """ A testing mixin. Right now, it just initializes logging. """

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


class BaseTest(_BaseTestMixin, tornado.testing.AsyncTestCase):
  """ Standard base test case for asynchronous code. """
  pass

class BaseHttpTest(_BaseTestMixin, tornado.testing.AsyncHTTPTestCase):
  """ Base test that starts an HTTP server. """

  def get_app(self):
    """ Gets the app to use for testing. In this case, it will be the one
    returned by server.make_app().
    Returns:
      The app to use for testing. """
    # We can just use all the default settings.
    return server.make_app({})
