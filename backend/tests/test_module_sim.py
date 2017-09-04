import logging

from ..module_sim import base_module
from ..module_sim import grow_module
from ..module_sim import simulator
from .. import serial_talker

from . import base_test


""" Tests for the mcu_sim package. """


logger = logging.getLogger(__name__)


class TestSimulator(base_test.BaseTest):
  """ Tests the Simulator, which simulates a module stack. """

  def __start_simulator(self, num_grow_modules):
    """ Starts the simulator running.
    Args:
      num_grow_modules: How many grow modules to add. 0 is acceptable. """
    # Add the base module.
    self.__sim.add_module(base_module.BaseModule)

    # Add as many grow modules as needed.
    for _ in range(0, num_grow_modules):
      self.__sim.add_module(grow_module.GrowModule)

    # Start the simulation running.
    self.__sim.start()

  def __wait_for_message(self, expected_message, prompt=None, expect_number=1):
    """ A utility function that waits to receive an expected message from the
    serial layer.
    Args:
      expected_message: The message we expect to receive. It can also be a list
                        of messages, in which case, the check will succeed if it
                        matches any one of them.
      prompt: An optional message to send before we wait to receive it.
      expect_number: The number of messages that we're waiting for. """
    # Make a message checker and add that as a handler.
    checker = self._make_message_checker(expected_message,
                                         expect_number=expect_number)
    self.__serial.add_message_handler(checker)

    # Send the prompt command if we need to.
    if prompt:
      self.__serial.write_existing_message(prompt)

    # Wait for the response.
    self.wait()
    # Clean up the handler.
    self.__serial.remove_message_handler(checker)

  def setUp(self):
    super().setUp()

    # Start the PSoC simulator.
    self.__sim = simulator.Simulator()

    # Initialize serial connection with simulator.
    device_name = self.__sim.get_serial_name()
    self.__serial = serial_talker.SerialTalker(115200, device=device_name,
                                               ioloop=self.io_loop)
    logger.info("Initialized connection to simulator.")

  def tearDown(self):
    self.__sim.force_exit()
    self.__serial.cleanup()

    super().tearDown()

  def test_ping(self):
    """ Tests that the simulator can receive and respond to a PING message. """
    self.__start_simulator(0)

    # Send a ping and expect to receive a response.
    expected = serial_talker.Message(serial_talker.Message.Ping, 1, "ack",
                                     source=2)
    prompt = serial_talker.Message("PING", 2)
    self.__wait_for_message(expected, prompt=prompt)

  def test_grow_module_ping(self):
    """ Tests that we can handle a ping command on the grow module. """
    self.__start_simulator(1)

    # We first expect to receive a discovery message.
    expected = serial_talker.Message(serial_talker.Message.ImAlive, 0,
                                     source=3)
    self.__wait_for_message(expected)

    # Now try pinging the base module.
    expected = serial_talker.Message(serial_talker.Message.Ping, 1, "ack",
                                     source=2)
    prompt = serial_talker.Message("PING", 2)
    self.__wait_for_message(expected, prompt=prompt)

    # Try pinging the grow module.
    expected = serial_talker.Message(serial_talker.Message.Ping, 1, "ack",
                                     source=3)
    prompt = serial_talker.Message("PING", 3)
    self.__wait_for_message(expected, prompt=prompt)

    # Try a broadcast ping.
    base_expected = serial_talker.Message(serial_talker.Message.Ping, 1, "ack",
                                          source=2)
    grow_expected = serial_talker.Message(serial_talker.Message.Ping, 1, "ack",
                                          source=3)
    prompt = serial_talker.Message("PING", 0)
    self.__wait_for_message([base_expected, grow_expected], prompt=prompt)

  def test_module_discovery(self):
    """ A more complicated test with multiple grow modules that ensures that the
    module discovery process is correctly simulated. """
    self.__start_simulator(3)

    # We expect to receive 3 discovery messages. (All the modules will have
    # their IDs set to 3 initially, so it will look like they are coming from
    # the same source.)
    disc_expected = serial_talker.Message(serial_talker.Message.ImAlive, 0,
                                          source=3)
    # Wait for all three of them, in an arbitrary order.
    self.__wait_for_message(disc_expected, expect_number=3)

    # Now the modules should have been assigned sequential IDs. Try pinging them
    # to make sure.
    expected = serial_talker.Message(serial_talker.Message.Ping, 1, "ack",
                                     source=3)
    prompt = serial_talker.Message("PING", 3)
    self.__wait_for_message(expected, prompt=prompt)

    expected = serial_talker.Message(serial_talker.Message.Ping, 1, "ack",
                                     source=4)
    prompt = serial_talker.Message("PING", 4)
    self.__wait_for_message(expected, prompt=prompt)

    expected = serial_talker.Message(serial_talker.Message.Ping, 1, "ack",
                                     source=5)
    prompt = serial_talker.Message("PING", 5)
    self.__wait_for_message(expected, prompt=prompt)
