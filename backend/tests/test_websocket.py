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

  def test_mcu_events(self):
    """ Tests that MCU events trigger the appropriate messages. """
    def receive_message(message):
      """ Used as a callback to read messages from the websocket.
      Args:
        message: The message that was received. """
      # None means the connection was closed.
      message = json.loads(message)
      self.assertEqual({"state": {"mcu_alive": False}}, message)
      self.stop()

    def send_message(*args):
      """ Sends a message after the socket is connected. """
      # Setting the mcu_alive state attribute should trigger a message.
      state.get_state().set("mcu_alive", False)

    connected = tornado.websocket.websocket_connect(self.__socket_url,
                    on_message_callback=receive_message)
    self.io_loop.add_future(connected, send_message)

    self.wait()
