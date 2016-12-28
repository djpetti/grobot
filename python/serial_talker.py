""" Communicate with the MCUs connected via the serial interface. """


import collections
import copy
import enum
import logging

import serial


logger = logging.getLogger(__name__)


class _Parser:
  """ Parses raw messages, and emits Message instances. """

  class State(enum.Enum):
    """ Keeps track of the parser state. """
    READING_START = "READING_START"
    READING_COMMAND = "READING_COMMAND"
    READING_SOURCE = "READING_SOURCE"
    READING_DEST = "READING_DEST"
    READING_FIELDS = "READING_FIELDS"
    DONE = "DONE"

  def __init__(self):
    # Any data that we've received, but haven't finished parsing yet.
    self.__unused = ""
    # The complete messages that were received.
    self.__parsed = collections.deque()

    # Keeps track of the state of the parser.
    self.__state = self.State.READING_START
    # The current message that we are working on.
    self.__message = Message()

  def __parse_char(self, char):
    """ Parses a single character.
    Args:
      char: The character to parse. """
    if (char == '<' and self.__state != self.State.READING_START):
      # If we get an open-bracket, that means that, regardless of where we are,
      # we've found the start of a message.
      logger.warning("Dropping partial message.")
      message = Message()

    if self.__state == self.State.READING_START:
      # Looking for the leading <.
      if char == '<':
        # We found the start.
        self.__state = self.State.READING_COMMAND

    elif self.__state == self.State.READING_COMMAND:
      # All bytes read are now part of the command, until we hit a slash.
      if char == '/':
        # We're done reading the comand.
        self.__state = self.State.READING_SOURCE
      else:
        self.__message.command += char

    elif self.__state == self.State.READING_SOURCE:
      # The source should be a single char.
      self.__message.source = int(char)
      self.__state = self.State.READING_DEST

    elif self.__state == self.State.READING_DEST:
      if char == '/':
        # The source and dest are separated from the rest of the message with a
        # slash.
        self.__state = self.State.READING_FIELDS
        # The parser needs an empty string to start with when parsing fields.
        self.__message.fields.append("")
      elif char == '>':
        # Some valid messages have no fields.
        self.__state = self.State.DONE
      else:
        # The dest should also be a single character.
        self.__message.dest = int(char)

    elif self.__state == self.State.READING_FIELDS:
      # All bytes are part of this particular field, until we hit a control
      # character.
      if char == '/':
        # We hit the end of this field.
        self.__message.fields.append("")
      elif char == '>':
        # We hit the end of the message.
        self.__state = self.State.DONE
      else:
        self.__message.fields[-1] += char

    # This is technically not part of the above if-else block. We want to run it
    # in EVERY case when we're in the done state.
    if self.__state == self.State.DONE:
      # We're done parsing the message. Save the complete message and reset.
      logger.debug("Finished parsing message.")

      self.__parsed.appendleft(copy.deepcopy(self.__message))
      self.__message = Message()

      self.__state = self.State.READING_START

  def parse(self, data):
    """ Parse some new data.
    Args:
      data: The raw data to parse. """
    logger.debug("Parsing new data: %s" % (data))

    for char in data:
      self.__parse_char(char)

  def get_message(self):
    """
    Returns:
      The earliest message received, or None if there are no new messages. """
    if not len(self.__parsed):
      # No new messages.
      return None

    return self.__parsed.pop()

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

  def __init__(self, *args):
    """ Checks the number of arguments, and defers to the proper method for
    construction. See the following two methods for the details. """
    if not len(args):
      # Default-initialize everything.
      self.__initialize_default()
    else:
      # Initialize with specific data.
      self.__initialize_with_data(*args)

  def __initialize_default(self):
    """ Default method that just initializes everything to null values. """
    self.command = ""
    self.source = 0
    self.dest = 0
    self.fields = []

  def __initialize_with_data(self, command, dest, *args):
    """ Represents a message to be sent over the interface.
    Args:
      command: The command mnemonic. Should be chosen from those defined above.
      dest: The destination of the command. 0 is broadcast, 1 is us, 2 is the
            system MCU.
      All further arguments will be interpreted as fields. """
    self.command = command
    self.source = 1
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

    # The parser we use to parse received messages.
    self.__parser = _Parser()

  def __del__(self):
    logger.info("Closing connection.")
    self.__conn.close()

  def write_command(self, *args, **kwargs):
    """ This is really just a convenience method for building a message and
    sending it to the MCU. All arguments are passed transparently to a
    Message intstance. """
    message = Message(*args, **kwargs)
    self.__write(message.get_raw())

  def read_response(self):
    """ Reads a command from the serial interface.
    Returns:
      The command, read and parsed into a message structure, or None if no new
      commands are available. """
    if not self.__conn.inWaiting():
      # No data to read.
      return None

    # Read as much data as we have available.
    data = self.__conn.read(self.__conn.inWaiting())
    self.__parser.parse(data)

    return self.__parser.get_message()

  def __write(self, message):
    """ Writes a raw message.
    Args:
      message: The message to write. """
    self.__conn.write(message)
