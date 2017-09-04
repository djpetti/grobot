from multiprocessing import Process
import logging
import os
import pty
import time

from .. import serial_talker


logger = logging.getLogger(__name__)


class Simulator:
  """ Manages the simulation and handles module communication. """

  def __init__(self):
    # Initialize serial.
    self.__conn, self.__device_name = self.__start_serial()

    # Keeps track of the modules in this simulation.
    self.__modules = set()

  def __del__(self):
    self.force_exit()

  def __start_serial(self):
    """ Initializes the serial connection.
    Returns:
      A handle to one end of the connection, as well as the device name for the
      other end. """
    our_end, their_end = pty.openpty()
    device_name = os.ttyname(their_end)
    logger.debug("Simulating MCU on %s." % (device_name))

    return our_end, device_name

  def __get_new_data(self):
    """ Gets new data from the serial layer.
    Returns:
      The message it got. """
    data = os.read(self.__conn, 1024)
    # Parse it.
    self.__parser.parse(data.decode("utf8"))

  def __run(self):
    """ Runs the simulator forever. """
    logger.info("Starting simulator process...")

    # Run one-time initialization for all modules.
    for module in self.__modules:
      module.on_startup()
    logger.debug("Initialized modules.")

    self.__parser = serial_talker.Parser()
    while True:
      # Get the next message from the serial layer.
      self.__get_new_data()
      if self.__parser.has_message():
        message = self.__parser.get_message()
        logger.debug("Got message: %s" % (message.get_raw()))

        # Handle the message.
        self.__handle_message(message, None)

      # Having a little delay is more realistic.
      time.sleep(0.01)

  def __handle_message(self, message, source_module):
    """ Passes a message to all simulated modules.
    Args:
      message: The message to handle.
      source_module: The module that this message is coming from. Can be None if
                     it's coming from the serial link. """
    for module in self.__modules:
        if module == source_module:
          # We never echo back to ourselves.
          continue
        module.check_and_handle_message(message)

  def write_message(self, command, source_module, dest, *args):
    """ Creates a writes a message.
    Args:
      command: The command for the message.
      source_module: The module this message is coming from.
      dest: The destination address of the message.
      All further args will be interpreted as field values. """
    source_id = source_module.get_id()
    message = serial_talker.Message(command, dest, *args, source=source_id)

    if (dest == 1 or dest == 0):
      # If we're sending to Prime, we have to write it onto the serial link. (A
      # special case is if we're writing a broadcast message, in which case we
      # have to do both options.)
      raw_message = message.get_raw()

      # Write all of it.
      total_written = 0
      while total_written < len(raw_message):
        to_write = raw_message[total_written:].encode("utf8")
        total_written += os.write(self.__conn, to_write)

    if (dest != 1 or dest == 0):
      # Otherwise, we can save time and just pass it directly to the relevant
      # module.
      self.__handle_message(message, source_module)

  def get_serial_name(self):
    """
    Returns:
      The name of the device that code should connect to to talk to the
      simulator. """
    return self.__device_name

  def force_exit(self):
    """ Forces the simulator to exit now. """
    if self.__sim_process.is_alive():
      logger.info("Terminating simulator process.")
      self.__sim_process.terminate()

  def add_module(self, module_class, **kwargs):
    """ Shortcut for adding a new module to the simulation.
    Args:
      module_class: The class of the module to add.
      Any kwargs will be forwarded to the module constructor. """
    logger.info("Adding new module '%s'..." % (module_class.__name__))
    module = module_class(self, **kwargs)

    self.__modules.add(module)

  def start(self):
    """ Starts the simulation actually running. Should be called after all
    modules are added and setup is complete. """
    # Fork off a separate process that does the simulation.
    self.__sim_process = Process(target=self.__run)
    self.__sim_process.start()
