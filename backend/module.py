import logging
import random

from .serial_talker import Message


logger = logging.getLogger(__name__)


class Module:
  """ Represents a single module. """

  def __init__(self, module_id, permanent_id):
    """
    Args:
      module_id: The module's ID, which is also it's I2C slave address.
      permanent_id: The module's permanent ID, which is stored in flash, and
                    generally set only once during the module's lifetime. """
    self.__id = -1
    self.__permanent_id = -1

    self.set_id(module_id)
    self.set_permanent_id(permanent_id)

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

  def gen_permanent_id(self):
    """ The permanent ID is different from the module ID used for communication
    in that it is stored in the MCU flash and persistent accross resets. It is a
    randomly-generated 32-bit number, and is used to uniquely identify modules
    so that module-related information can be stored accross power cycles. This
    method generates a new one. The generated permanent ID is automatically set
    for this module.
    Returns:
      The generated permanent ID. """
    permanent_id = random.getrandbits(32)
    self.__permanent_id = permanent_id

    return self.__permanent_id

  def set_permanent_id(self, permanent_id):
    """ Sets the permanent ID for this module.
    Args:
      permanent_id: The new permanent ID. """
    logger.debug("Changing permanent ID from %d to %d." % (self.__permanent_id,
                                                           permanent_id))
    self.__permanent_id = permanent_id

  def get_permanent_id(self):
    """
    Returns:
      The currently set permanent ID. """
    return self.__permanent_id


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
    self.__serial.add_message_handler(self.__common_handler)

  def __get_module_by_id(self, module_id):
    """ Gets a particular module by its ID.
    Args:
      module_id: The ID of the module.
    Returns:
      The module with that ID. """
    for module in self.__modules:
      if module.get_id() == module_id:
        return module

    # This has got to be a programming error.
    raise KeyError("No module with ID %d." % (module_id))

  def __common_handler(self, message):
    """ Handles all relevant messages coming from the modules.
    Args:
      message: The message to handle. """

    if message.command == Message.ImAlive:
      # Handles incoming IMALIVE messages. It essentially runs the same
      # algorithm that the modules themselves run upon seeing this message, to
      # ensure that the IDs it sets for them here match the ones they choose for
      # themselves. The first field of this message is the module's currently
      # set permanent ID.
      self.add_module(int(message.fields[0]))

  def add_module(self, permanent_id):
    """ Adds a new module to the system. The module's permanent ID will also be
    automatically generated if it does not already exist.
    Args:
      permanent_id: The permanent ID of the module. """
    logger.info("Discovered new module.")

    # The newest module always gets assigned the lowest ID, which is 3 in this
    # case since 0 is broadcast, 1 is us, and 2 is the BSC.
    new_module = Module(3, permanent_id)

    # Increment all the other module IDs, since this is what they will do upon
    # receipt of the message.
    for module in self.__modules:
      module.increment_id()

    # Save the module.
    self.__modules.add(new_module)

    if not permanent_id:
      # We need to generate a permanent ID for this module.
      self.gen_permanent_id(new_module.get_id())

  def gen_permanent_id(self, module_id):
    """ Generates a new permanent ID for a module, and sends it to that module.
    Args:
      module_id: The (I2C) ID of the module. """
    module = self.__get_module_by_id(module_id)

    # Generate one.
    permanent_id = module.gen_permanent_id()
    logger.debug("Generated permanent ID for module %d: %d" % (module_id,
                                                               permanent_id))

    # Set it on the MCU.
    self.__serial.write_command(Message.SetPermanentId, module_id, permanent_id)

  def get_modules(self):
    """
    Returns:
      The set of modules currently attached. """
    return self.__modules
