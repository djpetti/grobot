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

  def __send_message(self):
    """ Sends a broadcast message when the state changes. """
    message = {"state": self.__state}
    websocket.GrobotWebSocket.broadcast_message(message)

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
      self.__send_message()

  def get(self, key):
    """ Returns the state item referenced by a particular key.
    Args:
      key: The key to get the state for. """
    return self.__state[key]

  def reset(self):
    """ Resets the entire state. """
    logger.debug("Resetting the global state.")
    previously_empty = len(self.__state)
    self.__state = {}

    if not previously_empty:
      self.__send_message()


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
