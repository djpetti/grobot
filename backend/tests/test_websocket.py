import json
import logging

import tornado.websocket

from . import base_test
from .. import state
from .. import websocket


""" Tests the WebSocket system. """


logger = logging.getLogger(__name__)


class GrobotWebSocketTest(base_test.BaseWebSocketTest):
  """ Tests the GrobotWebSocket class. """

  def test_message_callbacks(self):
    """ Tests that we can add callbacks for particular message types. """
    got_messages = 0
    def handle_test_messages(message, *args):
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

    self._connect_and_run(on_connect)
