import collections
import logging

import motor.motor_tornado

import tornado.gen
import tornado.ioloop
import tornado.testing

from .. import server
from .. import websocket


logger = logging.getLogger(__name__)


class _BaseTestMixin:
  """ A testing mixin. This does stuff that is common to all testing classes in
  this file. """

  def __init_database(self):
    """ Initializes a mongo database for testing. """
    client = motor.motor_tornado.MotorClient("localhost", 27018)

    my_ioloop = self.get_new_ioloop()

    # Clear the database completely to prevent interference between tests.
    @tornado.gen.coroutine
    def drop_database():
      """ Helper function to drop the database. """
      result = client.drop_database("grobot_test_database")
      return result
    my_ioloop.run_sync(drop_database)
    my_ioloop.close()

    self._db = client.grobot_test_database

  def setUp(self):
    # Some of the default tornado test classes need the database to be
    # functional when they initialize the app, so we do that here before we call
    # them.
    self.__init_database()

    # Since this is a mixin, we have to initialize the next thing in the MRO.
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

  def _make_message_checker(self, expected_message, expect_number=1):
    """ Creates a function that can be used to check that a serial
    message matches a particular pattern.
    Args:
      expected_message: A constructed message whose fields we expect to match
                        with the one received. Can also be a list of messages,
                        in which case the check will succeed if any of them
                        match.
      expect_number: How many of these messages we expect to receive. Defaults
                     to 1.
    Returns:
      A function that can be passed as a callback which will check
      the message. """
    # We treat singleton items as a list of size 1.
    if not isinstance(expected_message, collections.Iterable):
      expected_message = [expected_message]

    # Group by attribute for easy testing.
    commands = []
    dests = []
    sources = []
    fields = []
    for message in expected_message:
      commands.append(message.command)
      dests.append(message.dest)
      sources.append(message.source)
      fields.append(message.fields)

    num_messages = 0

    def message_checker(message):
      """ The actual message checking function.
      Args:
        message: The message to check. """
      nonlocal num_messages

      logger.debug("Checking message: %s, %d, %d, %s" % (message.command,
                                                         message.source,
                                                         message.dest,
                                                         message.fields))

      self.assertIn(message.command, commands)
      self.assertIn(message.dest, dests)
      self.assertIn(message.source, sources)
      self.assertIn(message.fields, fields)

      num_messages += 1
      if num_messages == expect_number:
        # We have received as many as we were waiting for, so we can stop.
        self.stop()

    return message_checker

class BaseHttpTest(_BaseTestMixin, tornado.testing.AsyncHTTPTestCase):
  """ Base test that starts an HTTP server. """

  def get_app(self):
    """ Gets the app to use for testing. In this case, it will be the one
    returned by server.make_app().
    Returns:
      The app to use for testing. """
    # We can just use all the default settings.
    return server.make_app({}, self._db)

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
