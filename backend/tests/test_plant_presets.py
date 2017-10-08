import logging
import os

from .. import plant_presets

from . import base_test


""" Tests the plant preset manager. """


logger = logging.getLogger()


class PlantPresetTest(base_test.BaseTest):
  """ Tests for the PlantPreset class. """

  # Example well-formed preset file.
  GOOD_PRESET_FILE = "test_preset_dir/good.yaml"
  MISSING_ATTRIBUTES = "test_preset_dir/missing_attributes.yaml"
  WRONG_TYPE = "test_preset_dir/wrong_type.yaml"

  def setUp(self):
    super().setUp()

    # Load a known-good set of presets.
    test_path = os.path.dirname(__file__)
    preset_path = os.path.join(test_path, self.GOOD_PRESET_FILE)
    self.__preset = plant_presets.PlantPreset(preset_path)

  def test_get_attributes(self):
    """ Tests that we can get the attributes set in the example file. """
    name, icon_url = self.__preset.get_name_and_icon()
    self.assertEqual("Example Plant", name)
    self.assertEqual("static/img/plant.png", icon_url)

    red, white, blue = self.__preset.get_lighting()
    self.assertEqual(255, red)
    self.assertEqual(255, white)
    self.assertEqual(255, blue)

    grow_days = self.__preset.get_grow_days()
    self.assertEqual(30, grow_days)

    daylight_hours = self.__preset.get_daylight_hours()
    self.assertEqual(16.0, daylight_hours)

  def test_missing_attributes(self):
    """ Tests that it handles a file with missing attributes correctly. """
    test_path = os.path.dirname(__file__)
    preset_path = os.path.join(test_path, self.MISSING_ATTRIBUTES)

    # Try loading it. It should fail.
    self.assertRaises(KeyError, plant_presets.PlantPreset, preset_path)

  def test_wrong_type(self):
    """ Tests that it handles a file where some attributes are of the wrong
    type. """
    test_path = os.path.dirname(__file__)
    preset_path = os.path.join(test_path, self.WRONG_TYPE)

    # Try loading it. It should fail.
    self.assertRaises(KeyError, plant_presets.PlantPreset, preset_path)

class PresetManagerTest(base_test.BaseTest):
  """ Tests for the PresetManager class. """

  def test_load(self):
    """ Tests that we can load the presets from a directory. """
    test_path = os.path.dirname(__file__)
    preset_dir = os.path.join(test_path, "test_preset_dir")
    # Even though some are invalid, it should not throw exceptions.
    manager = plant_presets.PresetManager(preset_dir)

    # Check that the right ones got loaded.
    self.assertEqual(1, manager.get_num_presets())

  def test_get_preset(self):
    """ Tests that we can get a preset by name. """
    test_path = os.path.dirname(__file__)
    preset_dir = os.path.join(test_path, "test_preset_dir")
    manager = plant_presets.PresetManager(preset_dir)

    # Try getting a preset.
    preset = manager.get_preset("Example Plant")
    name, _ = preset.get_name_and_icon()
    self.assertEqual("Example Plant", name)
