import logging
import os
import time

import tornado.gen
import tornado.ioloop
import tornado.testing

from . import test_serial
from .. import cron
from .. import serial_talker
from .. import state


""" Tests the periodic jobs. """


logger = logging.getLogger(__name__)


class CheckMcuAliveJobTest(test_serial.SerialTalkerTestBase):
  """ Tests for the CheckMcuAlive job. """

  def setUp(self):
    super().setUp()

    self.__got_state_change = False

    # Create job for testing.
    self.__job = cron.CheckMcuAliveJob(1, self._serial_talker,
                                       ioloop=self.io_loop)

  def tearDown(self):
    super().tearDown()

    # Force it to clean up before the test ends.
    self.__job.stop()

  def __wait_for_state_change(self, key, expected, timeout=5):
    """ Waits for the state to change.
    Args:
      key: The key to check.
      expected: The expected value of the key.
      timeout: How many ping cycles to wait before giving up. """
    # Wait for a state change.
    self.__got_state_change = False
    for i in range(0, timeout):
      self.wait()
      if self.__got_state_change:
        # Check it.
        self.assertEqual(expected, state.get_state().get(key))
        break

    else:
      # Give up.
      self.fail("State change did not happen.")

  def test_ping_gets_called(self):
    """ Tests that it actually sends a ping. """

    def receive_message(*args):
      """ Function to use as a callback that checks the message. """
      self._wait_for_serial("<PING/12>")
      self.stop()

    # Set the handler.
    self.io_loop.add_handler(self._conn, receive_message,
                             tornado.ioloop.IOLoop.READ)

    # Running the IOLoop should prompt it to send a ping.
    self.wait()

  def test_correct_state(self):
    """ Tests that it sets the global state correctly. """

    def receive_message(*args):
      """ Function to use as a callback that checks the message. """
      self._wait_for_serial("<PING/12>")
      self.stop()

    def state_change(state):
      """ Fired when the state changes. """
      self.__got_state_change = True
      self.stop()

    # Add a state callback that fires when the state changes.
    state.get_state().add_callback(state_change)
    # Set the handler.
    self.io_loop.add_handler(self._conn, receive_message,
                             tornado.ioloop.IOLoop.READ)

    # The state should be good initially.
    self.assertTrue(state.get_state().get("mcu_alive"))

    # Wait for change the state. It should now say that
    # the MCU is not responding.
    self.__wait_for_state_change("mcu_alive", False)

    # Write a response.
    os.write(self._conn, "<PING/21/ack>".encode("utf8"))

    # Wait for the state to change to true.
    self.__wait_for_state_change("mcu_alive", True)
