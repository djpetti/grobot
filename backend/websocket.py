""" Implements GroBot-related websocket features. """


import json
import logging

import tornado.websocket


logger = logging.getLogger(__name__)


class GrobotWebSocket(tornado.websocket.WebSocketHandler):
  """ Web socket subclass for use on the grobot. Handles most of the
  communication between the backend and the frontend. """

  # A list of the Websockets that are currently open.
  _open = set()
  # A list of the callbacks to use for each message type.
  _message_callbacks = {}

  @classmethod
  def broadcast_message(cls, message):
    """ Sends a message to every open socket.
    Args:
      message: The message to send. It will be automatically JSON encoded. """
    logger.debug("Writing broadcast message to %d clients." % (len(cls._open)))

    for conn in cls._open:
      conn.write_message(message)

  @classmethod
  def add_message_handler(cls, message_type, callback):
    """ Add a handler for a specific type of message from any socket.
    Args:
      message_type: The type of message that we want to handle.
      callback: The callback that we want to run when we get a message of that
                type. It should take only the message as an argument. """
    logger.debug("Adding callback for messages of type '%s'." % (message_type))
    cls._message_callbacks[message_type] = callback

  def open(self, *args, **kwargs):
    """ Open a new websocket. """
    super().open(*args, **kwargs)

    logger.info("Opening new WebSocket connection: %s" % self)
    # Keep a set of all open connections.
    self._open.add(self)

  def on_close(self):
    """ Called when a connection is closed. """
    logger.info("Closing WebSocket connection: %s" % (self))
    self._open.remove(self)

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

    if "type" not in message:
      logger.error("Message does not have 'type' attr. Ignoring.")
      return

    # If we have a callback for that type, do it.
    mtype = message["type"]
    if mtype in self._message_callbacks:
      self._message_callbacks[mtype](message)
    else:
      logger.warning("No callbacks for message of type '%s'." % (mtype))
