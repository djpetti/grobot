import logging
import random

from .. import module
from .. import state
from ..serial_talker import Message

from . import base_test
from . import test_module_sim

""" Tests the module management code. """


logger = logging.getLogger(__name__)


class ModuleTest(base_test.BaseTest):
  """ Tests for the Module class. """

  def setUp(self):
    super().setUp()

    # Clear the global state, since the module system writes stuff in here.
    state.get_state().reset()

    # Make a module for testing.
    self.__module = module.Module(self._db.modules, -1, -1)

  def test_increment(self):
    """ Tests that the ID incrementing functionality works. """
    self.__module.set_id(1)
    self.assertEqual(1, self.__module.get_id())

    self.__module.increment_id()
    self.assertEqual(2, self.__module.get_id())

  def test_permanent_id(self):
    """ Tests that the permanent ID functionality works. """
    self.__module.set_permanent_id(42)
    self.assertEqual(42, self.__module.get_permanent_id())

    # Try generating a new one.
    random.seed(10)
    expected = random.getrandbits(32)

    random.seed(10)
    self.assertEqual(expected, self.__module.gen_permanent_id())
    self.assertEqual(expected, self.__module.get_permanent_id())

  def test_permanent_id_state_update(self):
    """ Tests that the global state gets updated when we set the permanent ID.
    """
    my_state = state.get_state()

    # Check that it created an entry for the initial permanent ID.
    self.assertEqual({}, my_state.get("modules", -1))

    # Changing the permanent ID should remove the first entry and add a new one.
    self.__module.set_permanent_id(1337)
    self.assertRaises(KeyError, my_state.get, "modules", -1)
    self.assertEqual({}, my_state.get("modules", 1337))

  def test_database_config(self):
    """ Tests that we can configure the module from the database once we have
    the permanent ID. """
    # Add a fake document for this module.
    document = {"permanent_id": 42}
    self._db.modules.add_document(document)
    self._db.modules.enable_test_stop(self)

    # Make sure the database gets probed when we set the permanent ID.
    self.__module.set_permanent_id(42)

    self.wait()

    # The collection should not have changed.
    documents = self._db.modules.get_documents()
    self.assertEqual(1, len(documents))
    self.assertEqual(42, documents[0]["permanent_id"])


class ModuleInterfaceTest(test_module_sim.SimulatorTestBase):
  """ Tests for the ModuleInterface class. """

  def setUp(self):
    super().setUp()

    # Make a module interface using the serial connection from the simulated
    # modules.
    self.__stack = module.ModuleInterface(self._serial, self._db)

  def test_discovery(self):
    """ Make sure module discovery works properly. """
    # Start the module simulation. It should immediately begin discovery.
    self._start_simulator(3)

    # Wait for the three discovery messages so we know the process is complete.
    # (The zero field is because the permanent ID will not be set by default.)
    disc_expected = Message(Message.ImAlive, 0, "0", source=3)
    self._wait_for_message(disc_expected, expect_number=3)

    # Now make sure the module interface handled this correctly.
    modules = self.__stack.get_modules()
    self.assertEqual(3, len(modules))

    # Make sure the IDs are set correctly.
    available_ids = set([3, 4, 5])
    for module in modules:
      self.assertIn(module.get_id(), available_ids)
      available_ids.remove(module.get_id())

  def test_permanent_id(self):
    """ Make sure that module permanent IDs work. """
    # Start the module simulation.
    self._start_simulator(1)

    # Seed the RNG so we can control what ID it picks.
    random.seed(10)
    expected_id = random.getrandbits(32)
    random.seed(10)

    # Wait for the discovery message. The permanent ID should not be set.
    disc_expected = Message(Message.ImAlive, 0, "0", source=3)
    self._wait_for_message(disc_expected)

    # Make sure the module interface handled this correctly.
    modules = self.__stack.get_modules()
    self.assertEqual(1, len(modules))

    for module in modules:
      # It should pick a new, "random" ID.
      self.assertEqual(expected_id, module.get_permanent_id())

    # The simulated module should also reflect this change.
    perm_id_prompt = Message(Message.GetPermanentId, 3)
    perm_id_expected = Message(Message.GetPermanentId, 1, str(expected_id),
                               source=3)
    self._wait_for_message(perm_id_expected, prompt=perm_id_prompt)

    # Reset the simulation. This time, specify a permanent ID.
    self._reset_simulator()
    self.__stack.clear_modules()
    self._start_simulator(1, permanent_id=42)

    disc_expected = Message(Message.ImAlive, 0, "42", source=3)
    self._wait_for_message(disc_expected)

    # Make sure the module interface reflects this.
    modules = self.__stack.get_modules()
    for module in modules:
      self.assertEqual(42, module.get_permanent_id())
