import logging

from . import websocket


logger = logging.getLogger(__name__)


class State:
  """ A container for global application state that is not written to the
  database. This is mostly just a wrapper around a Python dictionary, with
  methods that can be easily passed as callbacks. It also automatically sends a
  broadcast message on the websocket when the state changes. """

  def __init__(self):
    # This dictionary actually stores the state.
    self.__state = {}

    # Will be run when the state changes.
    self.__callbacks = set()
    # The default callback is to send a message on the websocket.
    self.add_callback(self.__send_message)

    # Add the state callback.
    websocket.GrobotWebSocket.add_message_handler("state",
                                                  self.__state_callback)

  def __send_message(self, state):
    """ Sends a broadcast message when the state changes.
    Args:
      state: The new state. """
    message = {"type": "state", "state": state}
    websocket.GrobotWebSocket.broadcast_message(message)

  def __state_callback(self, message, client):
    """ Callback that sends back the state when a client sends a state message.
    Args:
      message: The message received.
      client: The client that sent the message. """
    logger.debug("Sending state to %s, which requested it." % (client))
    client.write_message({"type": "state", "state": self.__state})

  def __run_callbacks(self):
    """ Run registered callbacks when the state changes. """
    for callback in self.__callbacks:
      # Copy the state so they can't mutate it.
      callback(self.__state.copy())

  def set(self, key, value):
    """ Sets a particular item in the state.
    Args:
      key: The name of the item to set.
      value: The value of the item to set. """
    changed = True
    if (key in self.__state and value == self.__state[key]):
      changed = False

    logger.debug("Setting state '%s' to '%s'." % (key, value))
    self.__state[key] = value

    if changed:
      self.__run_callbacks()

  def get(self, key):
    """ Returns the state item referenced by a particular key.
    Args:
      key: The key to get the state for. """
    return self.__state[key]

  def reset(self):
    """ Resets the entire state, and removes non-default callbacks. Note that
    this does trigger a state change message to be send on the websocket,
    however. """
    logger.debug("Resetting the global state.")
    previously_empty = (len(self.__state) == 0)
    self.__state = {}

    # Remove callbacks.
    self.__callbacks = set()
    self.add_callback(self.__send_message)

    if not previously_empty:
      self.__run_callbacks()

  def add_callback(self, callback):
    """ Add a callback, which will be run every time the state changes. It will
    be passed the new state dictionary as an argument.
    Args:
      callback: The callback to run. """
    logger.info("Adding new state change callback: %s" % (callback.__name__))
    self.__callbacks.add(callback)

  def remove_callback(self, callback):
    """ Remove a registered callback.
    Args:
      callback: The callback to remove. """
    if callback not in self.__callbacks:
      raise KeyError("Callback %s is not registered." % (callback.__name__))
    self.__callbacks.pop(self.__callback)


# The singleton state instance, stored at the module level.
__state_single = None

def get_state():
  """ Returns:
    A singleton state instance. Will be created if it doesn't already exist. """
  global __state_single

  if not __state_single:
    logger.info("Initializing new global state...")
    __state_single = State()

  return __state_single
