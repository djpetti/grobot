from multiprocessing import Process
import logging
import os
import pty

from .. import serial_talker


logger = logging.getLogger(__name__)


class Psoc:
  """ Simulates the PSOC microcontroller over a serial connection. """

  def __init__(self):
    # Initialize serial.
    self.__conn, self.__device_name = self.__start_serial()

    # Fork off a separate process that simulates the MCU.
    self.__mcu_process = Process(target=self.__run)
    self.__mcu_process.start()

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

  def __write_message(self, command, dest, *args):
    """ Creates a writes a message.
    Args:
      command: The command for the message.
      dest: The destination address of the message.
      All further args will be interpreted as field values. """
    message = serial_talker.Message(command, dest, *args, source=2)
    raw_message = message.get_raw()

    # Write all of it.
    total_written = 0
    while total_written < len(raw_message):
      to_write = raw_message[total_written:].encode("utf8")
      total_written += os.write(self.__conn, to_write)

  def __handle_ping(self, message):
    """ Handle a ping message.
    Args:
      message: The message to handle. """
    # Write a ping response message.
    self.__write_message("PING", 1, "ack")

  def __run(self):
    """ Runs the simulator forever. """
    logger.info("Starting simulator process...")

    self.__parser = serial_talker.Parser()
    while True:
      # Get the next message from the serial layer.
      self.__get_new_data()
      if self.__parser.has_message():
        message = self.__parser.get_message()
        logger.debug("Got message: %s" % (message.get_raw()))

        # Handle the message.
        if message.command == serial_talker.Message.Ping:
          self.__handle_ping(message)

  def get_device_name(self):
    """
    Returns:
      The name of the device that code should connect to to talk to the
      simulator. """
    return self.__device_name

  def force_exit(self):
    """ Forces the simulator to exit now. """
    if self.__mcu_process.is_alive():
      logger.info("Terminating simulator process.")
      self.__mcu_process.terminate()
