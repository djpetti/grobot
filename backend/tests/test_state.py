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

  def test_callbacks(self):
    """ Tests that state callbacks work. """
    def test_callback(state):
      """ Simple callback for state testing.
      Args:
        state: The new state dictionary. """
      self.assertEqual(1, state["test_key"])
      self.stop()

    my_state = state.get_state()

    # Add the callback.
    my_state.add_callback(test_callback)
    # It should get run when we change the state.
    my_state.set("test_key", 1)

class StateTestWithWebsocket(base_test.BaseWebSocketTest):
  """ Tests for the state class that integrate with websockets. """

  def setUp(self):
    super().setUp()

    # Clear the state.
    state.get_state().reset()

  def test_state_change_events(self):
    """ Tests that state change events trigger the appropriate messages. """
    def receive_message(message):
      """ Used as a callback to read messages from the websocket.
      Args:
        message: The message that was received. """
      message = json.loads(message)
      self.assertEqual({"type": "state", "state": {"mcu_alive": False}},
                       message)
      self.stop()

    def on_connect(*args):
      """ Sends a message after the socket is connected. """
      # Setting the mcu_alive state attribute should trigger a message.
      state.get_state().set("mcu_alive", False)

    self._connect_and_run(on_connect, receive_message)

  def test_state_callback(self):
    """ Tests that we can force it to send us state information by making a
    request. """
    def receive_message(message):
      """ Used as a callback to receive messages from the websocket.
      Args:
        message: The message that was received. """
      message = json.loads(message)
      self.assertEqual(message["type"], "state")
      self.assertIn("state", message)

      self.stop()

    def on_connect(future):
      """ Sends a state message after the socket is connected.
      Args:
        future: The connection future. """
      message = {"type": "state"}

      socket = future.result()
      socket.write_message(json.dumps(message))

    self._connect_and_run(on_connect, receive_message)
