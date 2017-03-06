import logging
import os

import tornado.ioloop

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

    # Create job for testing.
    self.__job = cron.CheckMcuAliveJob(1, self._serial_talker,
                                       ioloop=self.io_loop)

  def tearDown(self):
    super().tearDown()

    # Force it to clean up before the test ends.
    self.__job.stop()

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

    # Set the handler.
    self.io_loop.add_handler(self._conn, receive_message,
                             tornado.ioloop.IOLoop.READ)

    # The state should be good initially.
    self.assertTrue(state.get_state().get("mcu_alive"))

    # Wait for it to ping twice. It should now say that the MCU is not
    # responding.
    self.wait()
    self.wait()
    self.assertFalse(state.get_state().get("mcu_alive"))

    # Write a response.
    os.write(self._conn, "<PING/21/ack>".encode("utf8"))

    # Wait for it to ping again.
    self.wait()

    # The state should be good again.
    self.assertTrue(state.get_state().get("mcu_alive"))
