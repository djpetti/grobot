""" Presets for growing different types of plants. """

# TODO (danielp): All parameters need to be determined either experimentally, or
# from Dr. Pocock.

import logging
import os


logger = logging.getLogger(__name__)


import yaml
try:
  from yaml import CLoader as Loader
except ImportError:
  logger.warning("Falling back on pure Python yaml parser.")
  from yaml import Loader


class PlantPreset:
  """ Represents a set of presets for a particular type of plant. """

  def __init__(self, preset_file):
    """
    Args:
      preset_file: The YAML file containing the plant preset information. """
    logger.debug("Loading plant preset info from '%s'." % (preset_file))

    # Load the file.
    yaml_file = open(preset_file)
    raw_data = yaml.load(yaml_file, Loader=Loader)

    logger.debug("Loaded plant preset data: %s" % (raw_data))
    self.__set_from_file_data(raw_data)

  def __str__(self):
    # Use the name when converting to a string.
    return "<Preset: %s>" % (self.__plant_name)

  def __get_preset(self, data, key, type_conv=None):
    """ Gets a specific preset value.
    Args:
      data: The raw loaded data.
      key: The key of the preset.
      type_conv: Optional function to convert the value to a desired type.
    Returns:
      The preset value. """
    if key not in data:
      error = "Preset file missing key '%s'." % (key)
      logger.error(error)
      raise KeyError(error)

    value = data[key]

    if type_conv:
      # Handle type conversion.
      try:
        value = type_conv(value)
      except ValueError:
        error = "Cannot convert key '%s' to type '%s'." % (key,
                                                           type_conv.__name__)
        logger.error(error)
        raise KeyError(error)

    return value

  def __set_from_file_data(self, data):
    """ Ingests the raw data loaded from the YAML file, and sets the preset
    attributes accordingly.
    Args:
      data: The raw loaded data from the YAML file. """
    # Load basic information.
    self.__plant_name = self.__get_preset(data, "name")
    self.__icon_url = self.__get_preset(data, "icon")

    # Load the lighting information.
    lighting = self.__get_preset(data, "lighting")
    self.__red_channel = self.__get_preset(lighting, "red", type_conv=int)
    self.__white_channel = self.__get_preset(lighting, "white", type_conv=int)
    self.__blue_channel = self.__get_preset(lighting, "blue", type_conv=int)

    # Load the grow timing information.
    timing = self.__get_preset(data, "timing")
    self.__grow_days = self.__get_preset(timing, "grow_days", type_conv=int)
    self.__daylight_hours = self.__get_preset(timing, "daylight_hours",
                                              type_conv=float)

  def get_name_and_icon(self):
    """
    Returns:
      The name and icon URL of a plant. """
    return (self.__plant_name, self.__icon_url)

  def get_lighting(self):
    """
    Returns:
      The lighting specified for the plant, in terms of (R, W, B). """
    return (self.__red_channel, self.__white_channel, self.__blue_channel)

  def get_grow_days(self):
    """
    Returns:
      The number of days this plant should be grown for. """
    return self.__grow_days

  def get_daylight_hours(self):
    """
    Returns:
      The number of hours each day that the lights should be on for. """
    return self.__daylight_hours


class PresetManager:
  """ Manages a set of plant presets. """

  def __init__(self, preset_dir):
    """
    Args:
      preset_dir: The directory in which the preset files are stored. """
    self.__preset_dir = preset_dir
    self.__presets = self.__load_presets()

  def __load_presets(self):
    """ Loads the presets from the preset directory.
    Returns:
      A dictionary mapping preset names to the corresponding PlantPreset
      instances. """
    # Validate the preset directory.
    if not os.path.exists(self.__preset_dir):
      error = "Can't find preset directory: %s" % (self.__preset_dir)
      logger.error(error)

      # Indicate that we have no presets.
      return {}

    presets = {}

    # Find and load all the preset files.
    for preset_file in os.listdir(self.__preset_dir):
      preset_path = os.path.join(self.__preset_dir, preset_file)

      preset = None
      try:
        preset = PlantPreset(preset_path)
      except KeyError:
        # Malformed preset file.
        logger.warning("Skipping malformed preset file: %s" % (preset_path))
        continue

      # Add the preset to the dictionary.
      name, _ = preset.get_name_and_icon()
      presets[name] = preset

    return presets

  def get_preset(self, name):
    """ Gets a preset by name.
    Args:
      name: The name of the preset.
    Returns:
      The PlantPreset instance for that preset. """
    try:
      return self.__presets[name]
    except KeyError:
      # Preset not found.
      error = "Could not find preset '%s'." % (name)
      logger.error(error)
      raise KeyError(error)

  def get_num_presets(self):
    """
    Returns:
      The total number of presets that were loaded successfully. """
    return len(self.__presets)
