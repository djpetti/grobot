from .. import serial_talker


class ModuleCommon:
  """ Common functionality between all types of modules. """

  def __init__(self, simulator):
    """
    Args:
      simulator: The Simulator to use this module with. """
    self._sim = simulator

    # The ID of this module.
    self._id = -1

  def __handle_ping(self):
    """ Handle a ping message. """
    # Write a ping response message.
    self._write_message(serial_talker.Message.Ping, 1, "ack")

  def _write_message(self, command, dest, *args):
    """ Shortcut for sending messages with us as the source.
    Args:
      command: The command for the message.
      dest: The destination address of the message.
      All further args will be interpreted as field values. """
    self._sim.write_message(command, self, dest, *args)

  def _handle_message(self, message):
    """ Handles a received message. Should be overridden by subclasses.
    Args:
      message: The received message. """
    if message.command == serial_talker.Message.Ping:
      # Respond to Ping requests.
      self.__handle_ping()

  def on_startup(self):
    """ Perform any functionality that needs to be done on system
    initialization. Must be implemented by a subclass. """
    raise NotImplementedError("on_startup must be implemented by a subclass.")

  def check_and_handle_message(self, message):
    """ Checks that a message is for us, and handles it if it is.
    Args:
      message: The message to check. """
    if (message.dest == self._id or message.dest == 0):
      # It's for us.
      self._handle_message(message)

  def get_id(self):
    """
    Returns:
      The ID of the module. """
    return self._id
