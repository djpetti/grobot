import logging

from .. import state

from . import base_test


""" Tests the state system. """


logger = logging.getLogger(__name__)


class StateTest(base_test.BaseTest):
  """ Tests for the State class. """

  def setUp(self):
    super().setUp()

    # Clear the state.
    state.get_state().reset()

  def test_singleton(self):
    """ Tests that the state works in a basic way. """
    my_state = state.get_state()
    # Make sure it's the same.
    self.assertEqual(my_state, state.get_state())

  def test_set_get(self):
    """ Tests setting and getting basic attributes. """
    my_state = state.get_state()

    my_state.set("test_key", 1)
    self.assertEqual(1, my_state.get("test_key"))
