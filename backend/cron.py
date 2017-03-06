""" Functionality that has to be repeated by the backend at set times. """


import logging

import tornado.ioloop

from .serial_talker import Message
from . import state


logger = logging.getLogger(__name__)


class Job:
  """ A simple class that schedules a periodic job. """
  def __init__(self, interval, ioloop=tornado.ioloop.IOLoop.current()):
    """
    Args:
      interval: How much to delay between job interations, in milliseconds. """
    self.__callback = tornado.ioloop.PeriodicCallback(self.run, interval,
                                                      io_loop=ioloop)
    logger.info("Starting new periodic callback...")
    self.__callback.start()

  def __del__(self):
    self.stop()

  def run(self):
    """ This is what actually gets run. """
    raise NotImplementedError("Run must be implemented by subclass.")

  def stop(self):
    """ Stops the callback. """
    if self.__callback.is_running():
      logger.info("Stopping periodic callback.")
      self.__callback.stop()


class CheckMcuAliveJob(Job):
  """ Periodically checks to make sure that the MCU responds to pings. """
  def __init__(self, interval, serial, ioloop=tornado.ioloop.IOLoop.current()):
    """
    Args:
      See superclass documentation.
      serial: The SerialTalker instance to use for communicating with the MCU.
    """
    self.__serial = serial
    # Add a callback for MCU messages.
    self.__serial.add_message_handler(self.__handle_serial_message)

    # Set the state appropriately to begin with.
    self.__state = state.get_state()
    self.__state.set("mcu_alive", True)

    # Whether we received a response to our most recent ping.
    self.__received_response = True

    super().__init__(interval, ioloop=ioloop)

  def __handle_serial_message(self, message):
    """ Handles a new message from the serial subsystem.
    Args:
      message: The message we received. """
    if (message.command == Message.Ping and \
        message.fields[0] == "ack"):
      logger.debug("Got ping response from MCU.")
      self.__state.set("mcu_alive", True)
      self.__received_response = True

  def run(self):
    # Check if we got a response since we last sent something.
    if not self.__received_response:
      logger.critical("MCU is not responding!")
      self.__state.set("mcu_alive", False)
    self.__received_response = False

    logger.info("Pinging the MCU...")
    self.__serial.write_command(Message.Ping, 2)
