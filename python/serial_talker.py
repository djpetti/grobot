""" Communicate with the MCUs connected via the serial interface. """


import functools
import logging

import serial


logger = logging.getLogger(__name__)


class Message:
  # Map raw command mnemonics to a more readable / easily changeable form.
  #
  # A Ping command is pretty straight-forward. When any device receives a Ping
  # command, it is compelled to send back a response to the sender. This can be
  # used to verify that a particular component is online.
  Ping = "PING"
  # A SetControllerId command is used by Prime to set the ID of a controller.
  # The controller will set its ID exactly once. After that, the ID is set, and
  # cannot be changed until the next power cycle.
  SetControllerId = "SETID"
  # A SetLedBrightness command does pretty much what the name implies.
  SetLedBrightness = "SETLED"
  # A SetMainPump command is used to turn the main system pump on and off.
  SetMainPump = "SETPMP"
  # A ForceDosingPumps command is used to manually force the ph and nutrient
  # dosing pumps to turn on or off. Currently, it is mainly used for testing and
  # demo situations, and not during normal system operation.
  ForceDosingPumps = "FNUTPH"
  # A SendSensorStatus command is used to control whether or not status messages
  # should be send regularly from the MCU. Prime can disable these if it is not
  # in a position to handle them.
  SendSensorStatus = "ENSTAT"

  def __init__(self, command, dest, *args):
    """ Represents a message to be sent over the interface.
    Args:
      command: The command mnemonic. Should be chosen from those defined above.
      dest: The destination of the command. 0 is broadcast, 1 is us, 2 is the
            system MCU.
      All further arguments will be interpreted as fields. """
    self.command = command
    self.dest = dest
    self.fields = args

  def get_raw(self):
    """ Returns:
      The raw message that can be sent over the serial interface. """
    # Create the raw message.
    raw = "<%s/1%d" % (self.command, self.dest)
    for field in self.fields:
      raw += "/"
      raw += str(field)
    raw += ">"

    logger.debug("Raw message: %s" % (raw))
    return raw


class SerialTalker:
  def __init__(self, baudrate, conn=None):
    """
    Args:
      baudrate: The baudrate to use for communication with the MCU.
      conn: Forces the use of a particular connection object. """
    self.__conn = conn
    if not self.__conn:
      self.__conn = serial.Serial("/dev/ttyS0", baudrate)
      logger.info("Initialized serial connection with MCU.")
    else:
      logger.info("Using user-provided connection object.")

  def __del__(self):
    logger.info("Closing connection.")
    self.__conn.close()

  def write_command(self, *args, **kwargs):
    """ This is really just a convenience method for building a message and
    sending it to the MCU. All arguments are passed transparently to a
    Message intstance. """
    message = Message(*args, **kwargs)
    self.__write(message.get_raw())

  def __write(self, message):
    """ Writes a raw message.
    Args:
      message: The message to write. """
    self.__conn.write(message)
