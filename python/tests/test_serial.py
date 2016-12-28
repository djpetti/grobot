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

  def write(self, message):
    """ Writes a message to the buffer. """
    self.__buffer.appendleft(message)

  def close(self):
    self.__buffer.clear()

  def get_command(self):
    """
    Returns:
      The earliest command that was written. """
    return self.__buffer.pop()

class SerialTalkerTest(unittest.TestCase):
  """ Tests for the SerialTalker class. """

  def setUp(self):
    # Create a SerialTalker with a dummy connection.
    self.__conn = TestConnection()
    self.__serial_talker = serial_talker.SerialTalker(0, conn=self.__conn)

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
