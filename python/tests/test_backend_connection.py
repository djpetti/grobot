import json
import socket
import threading
import unittest

import backend_connection


""" Tests for the backend_connection module. """


class ServerTest(unittest.TestCase):
  """ Tests for the Server class. """

  def setUp(self):
    # Create the server for testing.
    server_thread = threading.Thread(target=self.__start_server)
    server_thread.start()

    # Create a connection to the server for testing.
    self.__conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # We might have to try a few times until it connects.
    while True:
      try:
        self.__conn.connect(("", 1337))
        break
      except socket.error:
        pass

    # We need to have accepted the connection before continuing.
    server_thread.join()

  def tearDown(self):
    # Clean up sockets.
    self.__conn.close()
    del self.__server

  def __start_server(self):
    """ Starts the server. Meant to be the target for a separate
    thread. """
    self.__server = backend_connection.Server(1337)

  def __send_fake_message(self, message):
    """ Sends a fake message to the server.
    Args:
      message: The message to send. Must be JSONable. """
    message = json.dumps(message)
    message = "<%s>" % (message)

    self.__conn.sendall(message.encode("utf8"))

  def test_simple_message(self):
    """ Make sure we can receive a simple message. """
    # No messages should be available to begin with.
    self.assertIsNone(self.__server.get_message())

    # First, we have to send the message from our end.
    message = [42, None, "hello"]
    self.__send_fake_message(message)

    # Now, we should be able to receive it.
    got_message = self.__server.get_message()
    self.assertEqual(message, got_message)

  def test_simple_message_send(self):
    """ Tests that we can send a single message. """
    # Send a message from our end.
    message = [42, None, "hello"]
    self.__server.send_message(message)

    # Make sure we can receive it at the other end.
    got_message = self.__conn.recv(4096)
    got_message = got_message.decode("utf8")
    self.assertEqual("<%s>" % (json.dumps(message)), got_message)

  def test_message_send_failure(self):
    """ Test that we can handle failed messages properly. """
    message = [42, None, "hello"]
    encoded_message = "<%s>" % (json.dumps(message))
    send_length = len(encoded_message)

    # Send messages until a send fails.
    while True:
      try:
        self.__server.send_message(message)
      except BlockingIOError:
        break

    # Receive some data. We will probably get a partial message at the end,
    # because it didn't fill up the buffer evenly.
    while True:
      got_message = self.__conn.recv(send_length).decode("utf8")
      if len(got_message) < send_length:
        # This must be the last partial message.
        break
      self.assertEqual(encoded_message, got_message)

    # We should be able to rectify the situation by sending another message,
    # which will force the transmission of the missing part.
    self.__server.send_message(message)

    missing_part = self.__conn.recv(send_length - len(got_message))
    missing_part = missing_part.decode("utf8")
    self.assertEqual(encoded_message, got_message + missing_part)

    # There should also be a whole nother complete message in there.
    got_message = self.__conn.recv(send_length).decode("utf8")
    self.assertEqual(encoded_message, got_message)
