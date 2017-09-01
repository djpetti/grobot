""" Communicate with the MCUs connected via the serial interface. """


import collections
import copy
import enum
import logging

import serial

import tornado.ioloop

from . import state


logger = logging.getLogger(__name__)


class Parser:
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

  def has_message(self):
    """
    Returns:
      True if we have at least one new message available, False otherwise. """
    return len(self.__parsed) != 0

  def get_message(self):
    """
    Returns:
      The earliest message received, or None if there are no new messages. """
    if not self.has_message():
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
  # An IMALIVE command is the first thing sent out by modules when
  # they finish initializing. It is used in the module discovery
  # process.
  ImAlive = "IMALIVE"
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

  def __init__(self, *args, source=1):
    """ Checks the number of arguments, and defers to the proper method for
    construction. See the following two methods for the details.
    Args:
      source: The source to use when sending messages. Defaults to 1. This
              argument should really only be used during testing. """
    self.__source = source

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
    self.source = self.__source
    self.dest = dest
    self.fields = args

  def get_raw(self):
    """ Returns:
      The raw message that can be sent over the serial interface. """
    # Create the raw message.
    raw = "<%s/%d%d" % (self.command, self.source, self.dest)
    for field in self.fields:
      raw += "/"
      raw += str(field)
    raw += ">"

    logger.debug("Raw message: %s" % (raw))
    return raw

class SerialTalker:
  # Maximum amount of data that will be put into the serial buffer at once.
  WRITE_BUFFER_MAX = 1000

  def __init__(self, baudrate, device="/dev/ttyS0",
               ioloop=tornado.ioloop.IOLoop.current()):
    """
    Args:
      baudrate: The baudrate to use for communication with the MCU.
      device: Forces the use of a particular serial device.
      ioloop: Forces the use of a particular IOLoop. """
    self.__cleaned_up = False

    # The callback to be used when a new message is read.
    self.__read_callbacks = set()
    # Buffer of data that is ready to be written.
    self.__write_buffer = ""

    self.__conn = None
    try:
      self.__conn = serial.Serial(device, baudrate, timeout=0, write_timeout=0)
    except serial.SerialException:
      logger.critical("Failed to initialize serial subsystem!")
      # Set that the MCU is not available.
      state.get_state().set("mcu_alive", False)

      raise ValueError("Serial Init Failed: Bad serial port?")

    logger.info("Initialized serial connection on %s at %d bps." % (device,
                                                                    baudrate))

    # The parser we use to parse received messages.
    self.__parser = Parser()

    # Setup IOLoop to process serial events.
    self.__ioloop = ioloop
    # Initially, we only trigger on readable events.
    self.__waiting_for_writable = False
    self.__ioloop.add_handler(self.__conn, self.__handle_serial_event,
                              tornado.ioloop.IOLoop.READ)

  def __del__(self):
    self.cleanup()

  def __handle_serial_event(self, fd, events):
    """ Handle a serial event and dispatch it to the right place. """
    if len(self.__write_buffer):
      # Room to write.
      self.__handle_serial_write_event()
    if self.__conn.in_waiting:
      # Room to read.
      self.__handle_serial_read_event()

  def __handle_serial_read_event(self):
    """ Handles read events from the serial connection. """
    # Read as much data as we have available.
    data = self.__conn.read(self.__conn.in_waiting)
    self.__parser.parse(data.decode("utf8"))

    while self.__parser.has_message():
      if not self.__read_callbacks:
        logger.warning("Got serial message but no callbacks set.")
        return

      message = self.__parser.get_message()
      for callback in self.__read_callbacks:
        # Run all the callbacks.
        callback(message)

  def __handle_serial_write_event(self):
    """ Handles writable events from the serial connection, and writes as much
    data as there is space to. It may write no data. """
    can_write = self.WRITE_BUFFER_MAX - self.__conn.out_waiting
    logger.debug("Writing %d bytes." % (can_write))

    # Write as much as we can.
    self.__conn.write(self.__write_buffer[:can_write].encode("utf8"))
    self.__write_buffer = self.__write_buffer[can_write:]

    # If we didn't write all of it, we want to listen for a writeable event so
    # we can try writing the rest.
    if (self.__write_buffer and not self.__waiting_for_writable):
      self.__waiting_for_writable = True
      self.__ioloop.update_handler(self.__conn,
                                   tornado.ioloop.IOLoop.READ |
                                   tornado.ioloop.IOLoop.WRITE)

    elif (not self.__write_buffer and self.__waiting_for_writable):
      self.__waiting_for_writable = False
      self.__ioloop.update_handler(self.__conn, tornado.ioloop.IOLoop.READ)

  def add_message_handler(self, callback):
    """ Adds a callback that will be called whenever a message is received.
    Args:
      callback: The callback that will be used. It should take an argument for
                the message. """
    logger.debug("Adding callback %s." % (str(callback)))
    self.__read_callbacks.add(callback)

  def remove_message_handler(self, callback):
    """ Removes a callback that was previously added.
    Args:
      callback: The callback that will be removed. """
    if callback not in self.__read_callbacks:
      raise KeyError("That callback was never added.")

    logger.debug("Removing callback %s." % (str(callback)))
    self.__read_callbacks.remove(callback)

  def write_command(self, *args, **kwargs):
    """ This is really just a convenience method for building a message and
    sending it to the MCU. All arguments are passed transparently to a
    Message intstance. It is asyncronous, and will return before the data is
    fully sent. """
    message = Message(*args, **kwargs)
    # Add it to the buffer so we can write when ready.
    self.__write_buffer += message.get_raw()
    # Try writing whatever we can right now.
    self.__handle_serial_write_event()

  def cleanup(self):
    """ Performs cleanup tasks such as closing the serial connection. """
    if self.__cleaned_up:
      return

    if self.__conn:
      logger.info("Closing connection.")
      self.__conn.close()

    self.__cleaned_up = True
