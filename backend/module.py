import logging

from .serial_talker import Message


logger = logging.getLogger(__name__)


class Module:
  """ Represents a single module. """

  def __init__(self, module_id):
    """
    Args:
      module_id: The module's ID, which is also it's I2C slave address. """
    self.__id = -1

    self.set_id(module_id)

  def set_id(self, module_id):
    """ Sets a new ID for the module.
    Args:
      module_id: The new module ID. """
    logger.debug("Changing module ID from %d to %d." % (self.__id, module_id))
    self.__id = module_id

  def get_id(self):
    """
    Returns:
      The currently set ID. """
    return self.__id

  def increment_id(self):
    """ Shortcut for incrementing the currently set ID. Useful during the
    discovery procedure, when this operation needs to happen a lot. """
    self.__id += 1
    logger.debug("Incrementing module ID to %d." % (self.__id))


class ModuleInterface:
  """ Handles global tasks pertaining to the entire set of modules. """

  def __init__(self, serial):
    """
    Args:
      serial: This is the SerialTalker to use for communicating with modules.
    """
    logger.info("Initializing module interface...")

    # Keeps track of all the modules we currently have.
    self.__modules = set()
    # Serial interface to use for all module communication.
    self.__serial = serial

    # Initialize the serial handler.
    self.__serial.add_message_handler(self.__imalive_handler)

  def __imalive_handler(self, message):
    """ Handles incoming IMALIVE messages. It essentially runs the same
    algorithm that the modules themselves run upon seeing this message, to
    ensure that the IDs it sets for them here match the ones they choose for
    themselves.
    Args:
      message: The received message. """
    if message.command == Message.ImAlive:
      # Add the new module.
      self.add_module()

  def add_module(self):
    """ Adds a new module to the system. """
    logger.info("Discovered new module.")

    # The newest module always gets assigned the lowest ID, which is 3 in this
    # case since 0 is broadcast, 1 is us, and 2 is the BSC.
    new_module = Module(3)

    # Increment all the other module IDs, since this is what they will do upon
    # receipt of the message.
    for module in self.__modules:
      module.increment_id()

    # Save the module.
    self.__modules.add(new_module)

  def get_modules(self):
    """
    Returns:
      The set of modules currently attached. """
    return self.__modules
