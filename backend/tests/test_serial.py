import logging
import os
import pty
import sys

import serial


from .. import serial_talker
from . import base_test


""" Tests serial interface and messaging. """


logger = logging.getLogger(__name__)


class SerialTalkerTest(base_test.BaseTest):
  """ Tests for the SerialTalker class. """

  def setUp(self):
    super().setUp()

    # Create a vitual TTY for this test.
    our_end, their_end = pty.openpty()
    device_name = os.ttyname(their_end)
    logger.debug("Opened device: %s" % (device_name))

    # Create a SerialTalker with a dummy connection.
    self.__serial_talker = serial_talker.SerialTalker(115200,
                                                      device=device_name,
                                                      ioloop=self.io_loop)
    # Other end of the connection.
    self.__conn = our_end

  def tearDown(self):
    super().tearDown()

    # Force it to clean up before the test ends.
    self.__serial_talker.cleanup()
    os.close(self.__conn)

  def __wait_for_serial(self, expected):
    """ Wait to receive from the serial, and compares it with an expected value.
    Args:
      expected: The expected value. """
    data = os.read(self.__conn, len(expected))
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
    self.__serial_talker.add_message_handler(receive_message)

    os.write(self.__conn, "<TEST/12>".encode("utf8"))

    self.wait()

  def test_multiple_callbacks(self):
    """ Tests parsing a message when we have more than one callback. """
    # Keeps track of whether a callback has already fired, so we know when to
    # call stop().
    callback_fired = False

    def receive_message1(message):
      """ Function to use as a callback reports when we receive a message.
      Args:
        message: The received message. """
      self.assertIsNotNone(message)

      nonlocal callback_fired
      if callback_fired:
        # Both callbacks happened. We can stop waiting.
        self.stop()
      else:
        # We still need to wait for the other one.
        callback_fired = True

    def receive_message2(message):
      """ Same as the above function, we just need two of them to test.
      Args:
        message: The received message. """
      receive_message1(message)

    # Add the two handlers.
    self.__serial_talker.add_message_handler(receive_message1)
    self.__serial_talker.add_message_handler(receive_message2)

    os.write(self.__conn, "<TEST/12>".encode("utf8"))

    self.wait()

    # It should let us remove both callbacks now without errors.
    self.__serial_talker.remove_message_handler(receive_message1)
    self.__serial_talker.remove_message_handler(receive_message2)
    # However, it should not let us remove them again.
    self.assertRaises(KeyError,
                      self.__serial_talker.remove_message_handler,
                      receive_message1)

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
    self.__serial_talker.add_message_handler(receive_message)

    os.write(self.__conn, "<TEST/12/42/None/hello>".encode("utf8"))

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
    self.__serial_talker.add_message_handler(receive_message)

    # Add one message, and a partial one.
    os.write(self.__conn, "<TEST/12/1><TEST/".encode("utf8"))
    self.wait()
    # Add the rest of the message.
    os.write(self.__conn, "12/2>".encode("utf8"))
    self.wait()
