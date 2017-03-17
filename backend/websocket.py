""" Implements GroBot-related websocket features. """


import json
import logging

import tornado.websocket


logger = logging.getLogger(__name__)


class GrobotWebSocket(tornado.websocket.WebSocketHandler):
  """ Web socket subclass for use on the grobot. Handles most of the
  communication between the backend and the frontend. """

  # A list of the Websockets that are currently open.
  _OPEN = set()

  @classmethod
  def broadcast_message(cls, message):
    """ Sends a message to every open socket.
    Args:
      message: The message to send. It will be automatically JSON encoded. """
    logger.debug("Writing broadcast message to %d clients." % (len(cls._OPEN)))

    for conn in cls._OPEN:
      conn.write_message(message)

  def open(self, *args, **kwargs):
    """ Open a new websocket. """
    super().open(*args, **kwargs)

    logger.info("Opening new WebSocket connection: %s" % self)
    # Keep a set of all open connections.
    self._OPEN.add(self)

  def on_close(self):
    """ Called when a connection is closed. """
    logger.info("Closing WebSocket connection: %s" % (self))
    self._OPEN.remove(self)

  def on_message(self, message):
    """ Invoked when a new message is received.
    Args:
      message: The message received. """
    logger.debug("Received message from frontend: %s" % (message))

    # Messages are all JSON-formatted, so we'll start by decoding it.
    try:
      message = json.loads(message)
    except json.decoder.JSONDecodeError:
      logger.error("Received malformed message. Ignoring.")
      return

    # Currently, our client doesn't send us anything...
