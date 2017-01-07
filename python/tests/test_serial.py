import collections
import unittest

import serial_talker


""" Tests serial interface and messaging. """


class TestConnection:
  """ A dummy object that mimics the behavior of a serial Connection object.
  This is so we can test things without having an actual serial interface
  running. """

  def __init__(self):
    self.__buffer = collections.deque()
    # The message that will be returned when we call read().
    self.__set_message = ""

  def read(self, length):
    """ Read the set message. """
    message = self.__set_message[:length]
    self.__set_message = self.__set_message[length:]
    return message

  def write(self, message):
    """ Writes a message to the buffer. """
    self.__buffer.appendleft(message)

  def close(self):
    self.__buffer.clear()
    self.__set_message = ""

  def inWaiting(self):
    """ Get how many bytes are ready to be read. """
    return len(self.__set_message)

  def get_command(self):
    """
    Returns:
      The earliest command that was written. """
    return self.__buffer.pop()

  def set_message(self, message):
    """ Set the message that will be returned when we call read.
    Args:
      message: The message to set. """
    self.__set_message = message

class SerialTalkerTest(unittest.TestCase):
  """ Tests for the SerialTalker class. """

  def setUp(self):
    # Create a SerialTalker with a dummy connection.
    self.__conn = TestConnection()
    self.__serial_talker = serial_talker.SerialTalker(0, conn=self.__conn)

  def tearDown(self):
    self.__conn.close()

  def test_simple_message(self):
    """ Tests sending a message with no fields. """
    self.__serial_talker.write_command("TEST", 2)

    message = self.__conn.get_command()
    self.assertEqual("<TEST/12>", message)

  def test_message_with_fields(self):
    """ Tests sending a message with fields. """
    self.__serial_talker.write_command("TEST", 2, 42, None, "hello")

    message = self.__conn.get_command()
    self.assertEqual("<TEST/12/42/None/hello>", message)

  def test_simple_message_read(self):
    """ Tests parsing a message without fields. """
    # Make sure that, initially, we get nothing.
    self.assertIsNone(self.__serial_talker.read_response())

    self.__conn.set_message("<TEST/12>")

    # Now, we should get something.
    message = self.__serial_talker.read_response()
    self.assertIsNotNone(message)
    self.assertEqual("TEST", message.command)
    self.assertEqual(1, message.source)
    self.assertEqual(2, message.dest)
    self.assertEqual([], message.fields)

  def test_message_read_with_fields(self):
    """ Tests parsing a message with fields. """
    # Make sure that, initially, we get nothing.
    self.assertIsNone(self.__serial_talker.read_response())

    self.__conn.set_message("<TEST/12/42/None/hello>")

    # Now, we should get something.
    message = self.__serial_talker.read_response()
    self.assertIsNotNone(message)
    self.assertEqual("TEST", message.command)
    self.assertEqual(1, message.source)
    self.assertEqual(2, message.dest)
    # Obviously, it's not going to know automatically how to convert stuff from
    # strings...
    self.assertEqual(["42", "None", "hello"], message.fields)

  def test_read_partial_message(self):
    """ Tests that it can properly parse messages that are split accross reads.
    """
    # Add one message, and a partial one.
    self.__conn.set_message("<TEST/12/1><TEST/")

    # We should get one message here.
    message = self.__serial_talker.read_response()
    self.assertIsNotNone(message)
    self.assertEqual("TEST", message.command)
    self.assertEqual(1, message.source)
    self.assertEqual(2, message.dest)
    self.assertEqual(["1"], message.fields)

    # We should not get any more for now.
    self.assertIsNone(self.__serial_talker.read_response())

    # Add the rest of the message.
    self.__conn.set_message("12/2>")

    # Now it should parse correctly.
    message = self.__serial_talker.read_response()
    self.assertIsNotNone(message)
    self.assertEqual("TEST", message.command)
    self.assertEqual(1, message.source)
    self.assertEqual(2, message.dest)
    self.assertEqual(["2"], message.fields)
