import json
import logging

import tornado.websocket

from . import base_test
from .. import state
from .. import websocket


""" Tests the WebSocket system. """


logger = logging.getLogger(__name__)


class GrobotWebSocketTest(base_test.BaseHttpTest):
  """ Tests the GrobotWebSocket class. """

  def setUp(self):
    super().setUp()

    # Create a WebSocket client for testing purposes.
    self.__socket_url = "ws://localhost:%d/app_socket" % (self.get_http_port())

  def __connect_and_run(self, connect_callback, receive_callback=None):
    """ Connects to a websocket, and runs a callback once the connection has
    been initiated.
    Args:
      connect_callback: The callback to run once the socket is connected.
      receive_message: The callback to run when a message is received. """
    connected = tornado.websocket.websocket_connect(self.__socket_url,
                    on_message_callback=receive_callback)
    self.io_loop.add_future(connected, connect_callback)

    self.wait()


  def test_mcu_events(self):
    """ Tests that MCU events trigger the appropriate messages. """
    def receive_message(message):
      """ Used as a callback to read messages from the websocket.
      Args:
        message: The message that was received. """
      # None means the connection was closed.
      message = json.loads(message)
      self.assertEqual({"type": "state", "state": {"mcu_alive": False}},
                       message)
      self.stop()

    def on_connect(*args):
      """ Sends a message after the socket is connected. """
      # Setting the mcu_alive state attribute should trigger a message.
      state.get_state().set("mcu_alive", False)

    self.__connect_and_run(on_connect, receive_message)

  def test_message_callbacks(self):
    """ Tests that we can add callbacks for particular message types. """
    got_messages = 0
    def handle_test_messages(message):
      """ Callback for handling messages of type 'test'. """
      # Check that the message is what we expected.
      self.assertEqual({"type": "test", "message": "monkey tacos"}, message)

      self.stop()

    def on_connect(future):
      """ Callback for when it connects. """
      # It will send this one first, but it should be ignored because the type
      # is wrong.
      message = json.dumps({"type": "not_test", "message": "farts"})
      message2 = json.dumps({"type": "test", "message": "monkey tacos"})

      socket = future.result()
      socket.write_message(message)
      socket.write_message(message2)

    # Add the handler.
    websocket.GrobotWebSocket.add_message_handler("test", handle_test_messages)

    self.__connect_and_run(on_connect)
