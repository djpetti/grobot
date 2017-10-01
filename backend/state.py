import logging

from . import websocket


logger = logging.getLogger(__name__)


class State:
  """ A container for global application state that is not written to the
  database. The state is defined as a nested tree structure, with methods that
  can be easily passed as callbacks. It also automatically sends a broadcast
  message on the websocket when the state changes. """

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

  def __get_item(self, keys, create=False):
    """ Gets an item indexed by a list of keys.
    Args:
      keys: The keys that index the item, from the top down.
      create: Whether to create any missing levels. If false, it will throw a
              key error instead.
    Returns: The item it found. """
    level = self.__state
    for key in keys:
      if key not in level:
        if create:
          # Create the missing item.
          level[key] = {}

        else:
          raise KeyError("Could not find key '%s' in state." % (key))

      level = level[key]

    return level

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

  def set(self, *args):
    """ Sets a particular item in the state.
    Args:
      The first arguments will be interpreted as the keys to the attribute that
      will be set. The last argument is interpreted as the value. """
    if len(args) < 2:
      raise AttributeError("Require at least one key and one value.")

    first_keys = args[:-2]
    last_key = args[-2]
    value = args[-1]

    level = self.__state
    if first_keys:
      # Find the appropriate level in the state tree. We want to get down to the
      # second-to-last one so we can modify the leaf node. (If we're modifying
      # something at the top leve, we don't need to worry about this.)
      level = self.__get_item(first_keys, create=True)

    logger.debug("Setting state '%s' to '%s'." % (args[:-1], value))

    if (last_key not in level or level[last_key] != value):
      level[last_key] = value
      self.__run_callbacks()

  def get(self, *args):
    """ Returns the state item referenced by a particular key.
    Args:
      The arguments will be interpreted as keys to the value that needs to be
      read. """
    return self.__get_item(args)

  def remove(self, *args):
    """ Removes an item from the state.
    Args:
      The arguments will be interpreted as keys to the value that needs to be
      removed. """
    logger.debug("Removing entry for %s from global state." % (str(args)))

    # Find up to the last level.
    first_keys = args[:-1]
    last_key = args[-1]

    last_level = self.__get_item(first_keys)

    # Remove it.
    last_level.pop(last_key)

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
