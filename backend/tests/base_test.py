import logging

import tornado.gen
import tornado.testing

from .. import server
from .. import websocket


logger = logging.getLogger(__name__)


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

class BaseWebSocketTest(BaseHttpTest):
  """ Convenience class for writing a test that uses a websocket. """

  def setUp(self):
    super().setUp()

    # WebSocket URL.
    self._socket_url = "ws://localhost:%d/app_socket" % (self.get_http_port())


  def _connect_and_run(self, connect_callback, receive_callback=None):
    """ Connects to a websocket, and runs a callback once the connection has
    been initiated.
    Args:
      connect_callback: The callback to run once the socket is connected.
      receive_message: The callback to run when a message is received. """
    def receive_wrapper(message):
      """ A simple wrapper that ignores None messages. Otherwise, we get a None
      message when we close the connection, which is sort of inconvenient for
      testing.
      Args:
        message: The received message. """
      if message is None:
        return

      receive_callback(message)

    connected = tornado.websocket.websocket_connect(self._socket_url,
                    on_message_callback=receive_wrapper)
    self.io_loop.add_future(connected, connect_callback)

    self.wait()

    # Close the connection.
    connected.result().close()

    def on_wait_done(*args):
      """ Runs until the wait period is done, and stops the IOLoop. """
      self.stop()

    # Give it some time to actually close.
    logger.info("Waiting for connections to close...")
    while True:
      wait_future = tornado.gen.sleep(0.1)
      self.io_loop.add_future(wait_future, on_wait_done)

      # Do the async delay.
      self.wait()

      if not websocket.GrobotWebSocket.get_num_clients():
        # Everything is closed.
        break