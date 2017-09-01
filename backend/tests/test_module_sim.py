import logging

from ..module_sim import base_module
from ..module_sim import simulator
from .. import serial_talker

from . import base_test


""" Tests for the mcu_sim package. """


logger = logging.getLogger(__name__)


class TestSimulator(base_test.BaseTest):
  """ Tests the Simulator, which simulates a module stack. """

  def setUp(self):
    super().setUp()

    # Start the PSoC simulator.
    self.__sim = simulator.Simulator()

    # Initialize serial connection with simulator.
    device_name = self.__sim.get_serial_name()
    self.__serial = serial_talker.SerialTalker(115200, device=device_name,
                                               ioloop=self.io_loop)
    logger.info("Initialized connection to simulator.")

    # Add the base module.
    self.__sim.add_module(base_module.BaseModule)

    # Start the simulation running.
    self.__sim.start()

  def tearDown(self):
    self.__sim.force_exit()
    self.__serial.cleanup()

    super().tearDown()

  def test_ping(self):
    """ Tests that the simulator can receive and respond to a PING message. """
    def receive_message(message):
      """ Handles a received message from the SerialTalker.
      Args:
        message: The message we received. """
      self.assertEqual(serial_talker.Message.Ping, message.command)
      self.assertEqual(1, message.dest)
      self.assertEqual(2, message.source)
      self.assertEqual(["ack"], message.fields)

      self.stop()

    # Add a message handler for receiving the ack message.
    self.__serial.add_message_handler(receive_message)

    # First, send a ping to it.
    self.__serial.write_command("PING", 2)

    # Wait for a response.
    self.wait()
