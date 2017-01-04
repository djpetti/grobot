import collections
import json
import logging
import socket


""" Implements a simple socket server for communicating with the web backend.
"""


logger = logging.getLogger(__name__)


class Server:
  """ A simple socket server. """

  def __init__(self, port):
    """ Initializes the server.
    Args:
      port: The port to listen on. """
    # Queue of complete, received messages.
    self.__messages = collections.deque()
    # Keeps track of any partially-sent messages that need to be retried.
    self.__partially_sent = collections.deque()

    self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__server.bind(("", port))
    self.__server.listen(1)

    # Wait for the web backend to connect.
    logger.info("Waiting for connection on %d..." % (port))
    self.__conn, self.__addr = self.__server.accept()
    logger.info("Got connection from %s." % (str(self.__addr)))

    # Don't block on socket operations.
    self.__conn.setblocking(0)

  def __del__(self):
    self.__server.close()

  def get_message(self):
    """ Receives as much data as is available, and parses it.
    Returns:
      The first complete message received if it exists, or None if it doesn't.
    """
    # Receive data in chunks.
    data = ""
    while True:
      try:
        received = self.__conn.recv(4096)
        data += received.decode("utf8")
      except BlockingIOError:
        # Nothing more to read.
        break

    if data:
      logger.debug("Got raw data: %s" % (data))

    # We use JSON to transfer data between here and NODE, with the same <>
    # scheme for delimitting messages that we use for the serial connection.
    raw_message = ""
    in_message = False
    for char in data:
      if char == "<":
        in_message = True
      elif char == ">":
        in_message = False
        # Un-JSON the message.
        self.__messages.appendleft(json.loads(raw_message))
      elif in_message:
        raw_message += char

    # Return a message if we have one.
    if len(self.__messages):
      return self.__messages.pop()
    else:
      return None

  def __try_send(self, message, resend):
    """ Try to send a message and handle problems appropriately. It raises a
    BlockingIOError if the full message was not sent successfully.
    Args:
      message: The message to try sending.
      resend: Whether we are resending the message, or sending a new message.
    """
    sent_bytes = None
    try:
      sent_bytes = self.__conn.send(message)
    except BlockingIOError:
      sent_bytes = 0

    if sent_bytes < len(message):
      logger.warning("Failed to send full message.")
      if resend:
        # If this was a resend that failed, it should go back on the end of the
        # queue.
        self.__partially_sent.append(message[sent_bytes:])
      else:
        # Otherwise, it goes at the front of the queue.
        self.__partially_sent.appendleft(message[sent_bytes:])

      raise BlockingIOError("Failed to send full message.")

  def send_message(self, message):
    """ Sends a message to the client. It will not block, so there is no chance
    of the Python system freezing if NODE goes down for some reason. If the data
    cannot be sent, it raises a BlockingIOError. In this case, it also
    automatically saves any part of the message that hasn't yet been sent, so
    this can be retried upon the next call to this method.
    Args:
      message: The message to send. It must be JSONable. """
    # Convert the message into a sendable format.
    message = json.dumps(message)
    message = "<%s>" % (message)
    message = message.encode("utf8")

    # First, check if there are any messages that need to be resent, and do
    # that.
    while len(self.__partially_sent):
      to_resend = self.__partially_sent.pop()
      try:
        self.__try_send(to_resend, True)
      except BlockingIOError as e:
        # If we can't resend our old messages, we can't safely send this one
        # either.
        self.__partially_sent.appendleft(message)
        raise e

    # Now, try sending it.
    self.__try_send(message, False)
