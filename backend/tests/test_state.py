import json
import logging

from .. import state

from . import base_test


""" Tests the state system. """


logger = logging.getLogger(__name__)


class StateTest(base_test.BaseTest):
  """ Tests for the State class. """

  def setUp(self):
    super().setUp()

    # Clear the state.
    state.get_state().reset()

  def test_singleton(self):
    """ Tests that the state works in a basic way. """
    my_state = state.get_state()
    # Make sure it's the same.
    self.assertEqual(my_state, state.get_state())

  def test_set_get(self):
    """ Tests setting and getting basic attributes. """
    my_state = state.get_state()

    my_state.set("test_key", 1)
    self.assertEqual(1, my_state.get("test_key"))

class StateTestWithWebsocket(base_test.BaseWebSocketTest):
  """ Tests for the state class that integrate with websockets. """

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

    self._connect_and_run(on_connect, receive_message)
