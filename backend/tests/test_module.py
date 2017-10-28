from unittest.mock import create_autospec, patch
import logging
import random

import tornado.concurrent

from .. import module
from .. import plant_presets
from .. import state
from ..serial_talker import Message

from . import base_test
from . import fake_db
from . import test_module_sim

""" Tests the module management code. """


logger = logging.getLogger(__name__)


class ModuleTest(base_test.BaseTest):
  """ Tests for the Module class. """

  # Default module state entry.
  DEFAULT_STATE = {"name": None, "icon_url": None,
                   "lighting": { \
                     "red": 0,
                     "white": 0,
                     "blue": 0 \
                   },
                   "timing": { \
                     "grow_days": 0,
                     "grow_days_elapsed": 0,
                     "daylight_hours": 0 \
                   }}

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
    self.assertEqual(self.DEFAULT_STATE, my_state.get("modules", -1))

    # Changing the permanent ID should remove the first entry and add a new one.
    self.__module.set_permanent_id(1337)
    self.assertRaises(KeyError, my_state.get, "modules", -1)
    self.assertEqual(self.DEFAULT_STATE, my_state.get("modules", 1337))

  def test_database_config_when_permanent_id_set(self):
    """ Tests that setting the permanent ID triggers configuration from the
    database. """
    # Add a fake document for this module.
    document = dict(self.DEFAULT_STATE)
    document["permanent_id"] = 42
    self._db.modules.add_document(document)
    self._db.modules.enable_test_stop(self)

    # Make sure the database gets probed when we set the permanent ID.
    self.__module.set_permanent_id(42)

    self.wait()

    # The collection should not have changed.
    documents = self._db.modules.get_documents()
    self.assertEqual(1, len(documents))
    self.assertEqual(42, documents[0]["permanent_id"])

  @patch.object(module.Module, "_add_or_update_module_in_db")
  @patch.object(module.Module, "_Module__update_state_from_module")
  def test_configure_from_preset(self, update_db_mock, update_state_mock):
    """ Tests that we an configure the module from a preset.
    Args:
      update_db_mock: The mock of the add_or_update_module_in_db function.
      update_state_mock: The mock of the update_state_from_module function. """
    # Fake a preset manager class.
    fake_preset = create_autospec(plant_presets.PlantPreset)

    # Set some return values for the preset methods.
    fake_preset.get_name_and_icon.return_value = ("Mr. Planty", "my_icon")
    fake_preset.get_lighting.return_value = (255, 254, 253)
    fake_preset.get_grow_days.return_value = 42
    fake_preset.get_daylight_hours.return_value = 12

    # Try running configure_from_preset,
    self.__module.configure_from_preset(fake_preset)

    # Now test that it set the attributes.
    self.assertEqual("Mr. Planty", self.__module._plant_name)
    self.assertEqual("my_icon", self.__module._plant_icon_url)
    self.assertEqual(255, self.__module._lighting_red)
    self.assertEqual(254, self.__module._lighting_white)
    self.assertEqual(253, self.__module._lighting_blue)
    self.assertEqual(42, self.__module._grow_days)
    self.assertEqual(12, self.__module._daylight_hours)

    # Make sure it tried to update the state and database.
    self.assertEqual(1, update_db_mock.call_count)
    self.assertEqual(1, update_state_mock.call_count)

  def test_module_db_update(self):
    """ Tests that we can update a module in the database. """
    # Set initial module attributes.
    self.__module._permanent_id = 1337
    self.__module._plant_name = "Mr. Planty"
    self.__module._plant_icon_url = "my_icon"
    self.__module._lighting_red = 255
    self.__module._lighting_white = 254
    self.__module._lighting_blue = 253
    self.__module._grow_days = 42
    self.__module._grow_days_elapsed = 1
    self.__module._daylight_hours = 12

    self._db.modules.enable_test_stop(self)

    # Try writing it to the database.
    self.__module._add_or_update_module_in_db()

    self.wait()

    # Make sure it got written.
    documents = self._db.modules.get_documents()
    self.assertEqual(1, len(documents))
    document = documents[0]

    self.assertEqual(self.__module._permanent_id, document["permanent_id"])
    self.assertEqual(self.__module._plant_name, document["name"])
    self.assertEqual(self.__module._plant_icon_url, document["icon_url"])
    self.assertEqual(self.__module._lighting_red, document["lighting"]["red"])
    self.assertEqual(self.__module._lighting_white, document["lighting"]["white"])
    self.assertEqual(self.__module._lighting_blue, document["lighting"]["blue"])
    self.assertEqual(self.__module._grow_days, document["timing"]["grow_days"])
    self.assertEqual(self.__module._grow_days_elapsed,
                     document["timing"]["grow_days_elapsed"])
    self.assertEqual(self.__module._daylight_hours,
                     document["timing"]["daylight_hours"])

  # For this test, we're going to stub out our fancy fake database with
  # something that always fails.
  @patch.object(fake_db.FakeCollection, "find_one_and_update")
  def test_module_db_update_failed(self, find_one_and_update_mock):
    """ Tests that it handles a database update failure.
    Args:
      find_one_and_update: Mock version of the database function. """
    # Set initial module attributes.
    self.__module._permanent_id = 1337
    self.__module._plant_name = "Mr. Planty"
    self.__module._plant_icon_url = "my_icon"
    self.__module._lighting_red = 255
    self.__module._lighting_white = 254
    self.__module._lighting_blue = 253
    self.__module._grow_days = 42
    self.__module._grow_days_elapsed = 1
    self.__module._daylight_hours = 12

    # Make the database operation fail. Since this is yeilded, we
    # have to correctly wrap our None return value in a future.
    future = tornado.concurrent.Future()
    future.set_result(None)
    find_one_and_update_mock.return_value = future

    self.__module._add_or_update_module_in_db()

    # This should throw an exception before it completes.
    self.assertRaises(module.DbError, self.wait)

  def test_module_configure_from_db(self):
    """ Tests that it can configure the module from the database. """
    # Fake document for testing.
    set_document = {}
    set_document["permanent_id"] = 42
    set_document["name"] = "Mr. Planty"
    set_document["icon_url"] = "my_icon"
    set_document["lighting"] = {"red": 255, "white": 254, "blue": 253}
    set_document["timing"] = {}
    set_document["timing"]["grow_days"] = 42
    set_document["timing"]["grow_days_elapsed"] = 1
    set_document["timing"]["daylight_hours"] = 12

    # Add the document to the database.
    self._db.modules.add_document(set_document)

    def operation_finished(document):
      """ Callback that gets run when the database operation is completed.
      Args:
        document: The document that was read from the database. """
      # There should be an database ID attribute.
      self.assertIn("_id", document)
      # Remove it, though, because it breaks the equality comparison.
      document.pop("_id")

      # Check that the documents match, first-of-all.
      self.assertEqual(set_document, document)

      # Check that the module got configured correctly.
      self.assertEqual(set_document["name"], self.__module._plant_name)
      self.assertEqual(set_document["icon_url"], self.__module._plant_icon_url)
      self.assertEqual(set_document["lighting"]["red"],
                       self.__module._lighting_red)
      self.assertEqual(set_document["lighting"]["white"],
                       self.__module._lighting_white)
      self.assertEqual(set_document["lighting"]["blue"],
                       self.__module._lighting_blue)
      self.assertEqual(set_document["timing"]["grow_days"],
                       self.__module._grow_days)
      self.assertEqual(set_document["timing"]["grow_days_elapsed"],
                       self.__module._grow_days_elapsed)
      self.assertEqual(set_document["timing"]["daylight_hours"],
                       self.__module._daylight_hours)

      self.stop()

    # Set the module's permanent ID manually so it finds the right entry.
    self.__module._permanent_id = 42

    # Run the database operation.
    self.__module._configure_from_db(callback=operation_finished)

    self.wait()

  def test_module_configure_from_db_no_document(self):
    """ Tests that it handles the case when there's no document for a module
    when configuring the module from the database. """
    # Don't add anything to the database.

    def operation_finished(document):
      """ Callback that gets run when the database operation is completed.
      Args:
        document: The document that was read from the database. """
      # No document should have been found.
      self.assertEqual(None, document)

      self.stop()

    # Run the database operation.
    self.__module._configure_from_db(callback=operation_finished)
    self.wait()


class ModuleInterfaceTest(test_module_sim.SimulatorTestBase):
  """ Tests for the ModuleInterface class. """

  def setUp(self):
    super().setUp()

    # Create a mock of the preset manager to pass in.
    self.__fake_presets = create_autospec(plant_presets.PresetManager)
    # Make a module interface using the serial connection from the simulated
    # modules.
    self.__stack = module.ModuleInterface(self._serial, self._db,
                                          self.__fake_presets)

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

  def test_set_from_preset(self):
    """ Tests that we can set a specified module from a preset. """
    # Set the return value of the fake get_preset function. It will just get
    # passed around opaquely, so we just need to make it something we can
    # easily check for.
    self.__fake_presets.get_preset.return_value = "preset"

    # Edit the modules set so we can find something with our permanent ID.
    fake_module = create_autospec(module.Module)
    fake_module.get_permanent_id.return_value = 42
    self.__stack._ModuleInterface__modules = set([fake_module])

    # Try running the FUT.
    self.__stack.set_from_preset(42, "my_preset")

    # Check that it looked for the preset.
    self.__fake_presets.get_preset.assert_called_once_with("my_preset")
    # Check that it set the preset on the module.
    fake_module.configure_from_preset.assert_called_once_with("preset")
