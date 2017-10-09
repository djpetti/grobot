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

  def test_multi_level(self):
    """ Tests getting and setting with a more complex state tree. """
    my_state = state.get_state()

    # Build a simple, two-level tree.
    my_state.set("test_group", "test_key", 1)
    self.assertEqual({"test_key": 1}, my_state.get("test_group"))
    self.assertEqual(1, my_state.get("test_group", "test_key"))

    # Try adding something else on the lower level.
    my_state.set("test_group", "test_key2", 2)
    self.assertEqual(1, my_state.get("test_group", "test_key"))
    self.assertEqual(2, my_state.get("test_group", "test_key2"))

    # Add another level.
    my_state.set("test_group", "test_inner_group", "test_key3", 3)
    self.assertEqual(1, my_state.get("test_group", "test_key"))
    self.assertEqual(2, my_state.get("test_group", "test_key2"))
    self.assertEqual(3, my_state.get("test_group", "test_inner_group",
                                     "test_key3"))

  def test_remove(self):
    """ Tests that we can remove items from the state. """
    my_state = state.get_state()

    # Add some items.
    my_state.set("test_key", 1)
    my_state.set("test_group", "test_key2", 2)

    # Try removing.
    my_state.remove("test_group")
    self.assertRaises(KeyError, my_state.get, "test_group")
    # The first one should still be there.
    self.assertEqual(1, my_state.get("test_key"))

    # Remove the first one too.
    my_state.remove("test_key")
    self.assertRaises(KeyError, my_state.get, "test_key")

  def test_callbacks_on_set(self):
    """ Tests that state callbacks work when we set an item. """
    def test_callback(key):
      """ Simple callback for state testing.
      Args:
        key: The key that was changed. """
      self.assertEqual(key, ["test_key"])
      self.stop()

    my_state = state.get_state()

    # Add the callback.
    my_state.add_callback(test_callback)
    # It should get run when we change the state.
    my_state.set("test_key", 1)

  def test_callbacks_on_remove(self):
    """ Tests that state callbacks work when we remove an item. """
    def test_callback(key):
      """ Simple callback for state testing.
      Args:
        key: The key that was changed. """
      # This should be empty, since we deleted a top-level key.
      self.assertEqual(key, [])
      self.stop()

    my_state = state.get_state()
    # Set an attrbiute.
    my_state.set("test_key", 1)

    # Add the callback.
    my_state.add_callback(test_callback)
    # Remove the attribute, which should fire the callback.
    my_state.remove("test_key")

  def test_callbacks_on_reset(self):
    """ Tests that state callbacks work when we reset the state. """
    def test_callback(key):
      """ Simple callback for state testing.
      Args:
        key: The key that was changed. """
      # This should be empty, since a reset always changes the top-level.
      self.assertEqual(key, [])
      self.stop()

    my_state = state.get_state()
    # Set an attribute.
    my_state.set("test_key", 1)

    # Add the callback.
    my_state.add_callback(test_callback)
    # Reset the state, which should fire the callback.
    my_state.reset()

  def test_stuttering_reset(self):
    """ Tests that a reset that does nothing doesn't fire a callback. """
    def test_callback(*args):
      """ Simple callback for state testing. """
      # This should never get run.
      self.fail("Callback should not have been run.")
      self.stop()

    my_state = state.get_state()
    # Add the callback.
    my_state.add_callback(test_callback)

    # Resetting an empty state does nothing.
    my_state.reset()

  def test_stuttering_set(self):
    """ Tests that a set that does nothing doesn't fire a callback. """
    def test_callback(*args):
      """ Simple callback for state testing. """
      # This should never get run.
      self.fail("Callback should not have been run.")
      self.stop()

    my_state = state.get_state()
    # Set an attribute.
    my_state.set("test_key", 1)
    # Add the callback.
    my_state.add_callback(test_callback)

    # Set the same thing again.
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
      self.assertEqual({"type": "state_change", "key": ["mcu_alive"]},
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
      self.assertEqual({}, message["state"])

      self.assertIn("key", message)
      self.assertEqual([], message["key"])

      self.stop()

    def on_connect(future):
      """ Sends a state message after the socket is connected.
      Args:
        future: The connection future. """
      message = {"type": "state"}

      socket = future.result()
      socket.write_message(json.dumps(message))

    self._connect_and_run(on_connect, receive_message)

  def test_state_partial_send(self):
    """ Tests that we can request a partial state update. """
    def receive_message(message):
      """ Used as a callback to receive messages from the websocket.
      Args:
        message: The message that was received. """
      message = json.loads(message)
      self.assertEqual(message["type"], "state")

      self.assertIn("state", message)
      self.assertEqual(1, message["state"])

      self.assertIn("key", message)
      self.assertEqual(["test_group", "test_key_1"], message["key"])

      self.stop()

    def on_connect(future):
      """ Sends a state message after the socket is connected.
      Args:
        future: The connection future. """
      message = {"type": "state", "key": ["test_group", "test_key_1"]}

      socket = future.result()
      socket.write_message(json.dumps(message))

    # Set up the state. We do this here before anything connects so it doesn't
    # trigger any callbacks.
    state.get_state().set("test_group", "test_key_1", 1)

    self._connect_and_run(on_connect, receive_message)
