import logging
import os

import serial_talker
import sys

import serial

import tornado.testing


""" Tests serial interface and messaging. """


logger = logging.getLogger(__name__)


class SerialTalkerTest(tornado.testing.AsyncTestCase):
  """ Tests for the SerialTalker class. """

  def setUp(self):
    super().setUp()

    # Check to make sure that virtual TTY is set up.
    if not os.path.exists("/dev/pts/1"):
      logger.critical("Cannot find virtual TTY. Please create it like \
                      `socat -d -d pty,raw,echo=0 pty,raw,echo=0 &`.")
      sys.exit(1)

    # Create a SerialTalker with a dummy connection.
    self.__serial_talker = serial_talker.SerialTalker(115200,
                                                      device="/dev/pts/1",
                                                      ioloop=self.io_loop)
    # Other end of the connection.
    self.__conn = serial.Serial("/dev/pts/2", baudrate=115200, timeout=1)

  def tearDown(self):
    self.__conn.close()

  def __wait_for_serial(self, expected):
    """ Wait to receive from the serial, and compares it with an expected value.
    Args:
      expected: The expected value. """
    data = self.__conn.read(len(expected))
    self.assertEqual(expected, data.decode("utf8"))

  def test_simple_message(self):
    """ Tests sending a message with no fields. """
    self.__serial_talker.write_command("TEST", 2)

    self.__wait_for_serial("<TEST/12>")

  def test_message_with_fields(self):
    """ Tests sending a message with fields. """
    self.__serial_talker.write_command("TEST", 2, 42, None, "hello")

    self.__wait_for_serial("<TEST/12/42/None/hello>")

  def test_simple_message_read(self):
    """ Tests parsing a message without fields. """
    def receive_message(message):
      """ Function to use as a callback that checks the message.
      Args:
        message: The received message. """
      self.assertIsNotNone(message)
      self.assertEqual("TEST", message.command)
      self.assertEqual(1, message.source)
      self.assertEqual(2, message.dest)
      self.assertEqual([], message.fields)

      self.stop()

    # Set the handler appropriately.
    self.__serial_talker.set_message_handler(receive_message)

    self.__conn.write("<TEST/12>".encode("utf8"))

    self.wait()

  def test_message_read_with_fields(self):
    """ Tests parsing a message with fields. """
    def receive_message(message):
      """ Function to use as a callback that checks the message.
      Args:
        message: The received message. """
      self.assertIsNotNone(message)
      self.assertEqual("TEST", message.command)
      self.assertEqual(1, message.source)
      self.assertEqual(2, message.dest)
      # Obviously, it's not going to know automatically how to convert stuff from
      # strings...
      self.assertEqual(["42", "None", "hello"], message.fields)

      self.stop()

    # Set the handler appropriately.
    self.__serial_talker.set_message_handler(receive_message)

    self.__conn.write("<TEST/12/42/None/hello>".encode("utf8"))

    self.wait()

  def test_read_partial_message(self):
    """ Tests that it can properly parse messages that are split accross reads.
    """
    message_num = 1
    def receive_message(message):
      """ Function to use as a callback that checks the message.
      Args:
        message: The received message. """
      nonlocal message_num

      # We should get one message here.
      self.assertIsNotNone(message)
      self.assertEqual("TEST", message.command)
      self.assertEqual(1, message.source)
      self.assertEqual(2, message.dest)

      # The two messages will be the same, aside from this field.
      self.assertEqual([str(message_num)], message.fields)
      message_num += 1

      self.stop()

    # Set the handler appropriately.
    self.__serial_talker.set_message_handler(receive_message)

    # Add one message, and a partial one.
    self.__conn.write("<TEST/12/1><TEST/".encode("utf8"))
    self.wait()
    # Add the rest of the message.
    self.__conn.write("12/2>".encode("utf8"))
    self.wait()
