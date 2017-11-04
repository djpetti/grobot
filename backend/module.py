import logging
import random

from tornado.ioloop import IOLoop
import tornado.gen

from pymongo import ReturnDocument

from . import state
from .serial_talker import Message


logger = logging.getLogger(__name__)


class DbError(Exception):
  """ Used when a database operation fails. """
  pass


class _ModuleDatabaseHelper:
  """ A base class for Module concerned specifically with database operations.
  This class exists mainly to split out some of the Module functionality and
  to make the Module class less unweildy. """

  def __init__(self, module_col):
    """
    Args:
      module_col: The module database collection. """
    self._col = module_col

  def __find_module(self):
    """ Finds a module by its permanent ID in the
    database.
    Returns:
      The found module future, or None if it found nothing. The result of this
      function is meant to be yielded from a coroutine. """
    query = {"permanent_id": self._permanent_id}
    return self._col.find_one(query)

  def _get_module_document(self):
    """
    Returns:
      A representation of the module that can be stored in the database. """
    module_doc = {"permanent_id": self._permanent_id,
                  "name": self._plant_name,
                  "icon_url": self._plant_icon_url,
                  "lighting": { \
                    "red": self._lighting_red,
                    "white": self._lighting_white,
                    "blue": self._lighting_blue \
                  },
                  "timing": { \
                    "grow_days": self._grow_days,
                    "grow_days_elapsed": self._grow_days_elapsed,
                    "daylight_hours": self._daylight_hours \
                  }}
    return module_doc

  def __set_module_from_document(self, module_doc):
    """ Sets a module's parameters from a document read out of the database.
    Args:
      module_doc: The module document. """
    logger.debug("Setting module params from: %s" % (module_doc))

    # Set the parameters.
    self._plant_name = module_doc["name"]
    self._plant_icon_url = module_doc["icon_url"]

    lighting = module_doc["lighting"]
    self._lighting_red = lighting["red"]
    self._lighting_white = lighting["white"]
    self._lighting_blue = lighting["blue"]

    timing = module_doc["timing"]
    self._grow_days = timing["grow_days"]
    self._grow_days_elapsed = timing["grow_days_elapsed"]
    self._daylight_hours = timing["daylight_hours"]

  def _add_or_update_module_in_db(self, callback=None):
    """ Will either update the existing entry for this module in the database,
    or add a new one if it does not exist yet. This executes database operations
    in a fire-and-forget sort of fashion. (Errors will be logged.)
    Args:
      callback: If provided, will run upon completion of the operation. It will
                be passed the new document from the database as an argument. """
    @tornado.gen.coroutine
    def do_update():
      """ Performs the actual update. See the documentation of the enclosing
      function. """
      # Get the document to set in the database.
      module_doc = self._get_module_document()

      # Update or create a new document.
      query = {"permanent_id": self._permanent_id}
      update = {"$set": module_doc}
      new_doc = yield self._col.find_one_and_update(query, update, upsert=True,
                          return_document=ReturnDocument.AFTER)
      logger.debug("New module document: %s" % (new_doc))

      if not new_doc:
        # A failed update.
        error = "Failed to update document for module %d." % \
                (self._permanent_id)
        logger.error(error)
        raise DbError(error)

      # Run the callback.
      if callback:
        callback(new_doc)

    # Perform this asynchronously using the ioloop.
    IOLoop.current().spawn_callback(do_update)

  def _configure_from_db(self, callback=None):
    """ Reads the module configuration out of the database, and updates the
    module accordingly. If it can't find the module, it will make no changes.
    This executes in a fire-and-forget fashion. (Errors will be logged.)
    Args:
      callback: If provided, will run upon completion of the operation. It will
                passed the document read from the database as an argument. """
    @tornado.gen.coroutine
    def do_configure():
      """ Performs the actual configuration. See documentation of the enclosing
      function. """
      # Look for the document.
      existing_doc = yield self.__find_module()

      if not existing_doc:
        # Technically, it's possible to get here, because Mongo acknowledges the
        # write before it's written to disk. However, this will only really
        # happen when we just created the document, in which case, we don't have
        # any data for this module anyway.
        logger.debug("No Mongo document for module. Asuming new.")

      else:
        logger.debug("Will set module %d config from database." % \
                    (self._permanent_id))
        self.__set_module_from_document(existing_doc)

      # Run the callback.
      if callback:
        callback(existing_doc)

    # Perform this asynchronously using the ioloop.
    IOLoop.current().spawn_callback(do_configure)


class Module(_ModuleDatabaseHelper):
  """ Represents a single module. """

  def __init__(self, module_col, module_id, permanent_id):
    """
    Args:
      module_col: The module collection in the database to use.
      module_id: The module's ID, which is also it's I2C slave address.
      permanent_id: The module's permanent ID, which is stored in flash, and
                    generally set only once during the module's lifetime. """
    super().__init__(module_col)

    # Current preset that is being used for this module.
    self._preset = None

    # The current name of whatever's growing in this module.
    self._plant_name = None
    # The current icon URL of the plant.
    self._plant_icon_url = None

    # The brightness of the lights in this module, from 0-255.
    self._lighting_red = 0
    self._lighting_white = 0
    self._lighting_blue = 0

    # Total days that this plant needs to grow for.
    self._grow_days = 0
    # How many of those days have elapsed.
    self._grow_days_elapsed = 0

    # How many hours of daylight this plant needs.
    self._daylight_hours = 0

    # Initialize these to something bogus so the logging works.
    self.__id = -1
    self._permanent_id = -1

    self.set_id(module_id)
    self.set_permanent_id(permanent_id)

  def __update_state_from_module(self):
    """ Updates the global state based on the module configuration. """
    # Get the module document.
    document = self._get_module_document()
    # We will index it by the permanent ID in the state.
    permanent_id = document.pop("permanent_id")

    logger.debug("Updating global state for module %d." % (permanent_id))

    state.get_state().set("modules", permanent_id, document)

  def set_id(self, module_id):
    """ Sets a new ID for the module.
    Args:
      module_id: The new module ID. """
    logger.debug("Changing module ID from %d to %d." % (self.__id, module_id))
    self.__id = module_id

  def get_id(self):
    """
    Returns:
      The currently set ID. """
    return self.__id

  def increment_id(self):
    """ Shortcut for incrementing the currently set ID. Useful during the
    discovery procedure, when this operation needs to happen a lot. """
    self.__id += 1
    logger.debug("Incrementing module ID to %d." % (self.__id))

  def gen_permanent_id(self):
    """ The permanent ID is different from the module ID used for communication
    in that it is stored in the MCU flash and persistent accross resets. It is a
    randomly-generated 32-bit number, and is used to uniquely identify modules
    so that module-related information can be stored accross power cycles. This
    method generates a new one. The generated permanent ID is automatically set
    for this module, and written into the database.
    Returns:
      The generated permanent ID. """
    permanent_id = random.getrandbits(32)
    self.set_permanent_id(permanent_id, new_module=True)

    return self._permanent_id

  def set_permanent_id(self, permanent_id, new_module=False):
    """ Sets the permanent ID for this module. Once this is set, it will try to
    read the module configuration from the database.
    Args:
      permanent_id: The new permanent ID.
      new_module: If this is set, it will not bother trying to configure from
                  database, which can be a nice optimization. """
    logger.debug("Changing permanent ID from %d to %d." % (self._permanent_id,
                                                           permanent_id))
    old_id = self._permanent_id
    self._permanent_id = permanent_id

    # Read our configuration out from the database once we have a permanent ID.
    if not new_module:
      self._configure_from_db()

    # Update the global state.
    my_state = state.get_state()
    try:
      # Remove an existing entry if it's there.
      my_state.remove("modules", old_id)
    except KeyError:
      pass

    # Add the updated entry.
    self.__update_state_from_module()

  def get_permanent_id(self):
    """
    Returns:
      The currently set permanent ID. """
    return self._permanent_id

  def configure_from_preset(self, preset):
    """ Configure this module from a preset.
    Args:
      preset: The preset to configure from. """
    logger.info("Configuring module %d from preset: '%s'" % \
                (self._permanent_id, str(preset)))
    self._preset = preset

    # Set all the attributes based on the preset values.
    self._plant_name, self._plant_icon_url = self._preset.get_name_and_icon()
    self._lighting_red, self._lighting_white, self._lighting_blue = \
        self._preset.get_lighting()
    self._grow_days = self._preset.get_grow_days()
    self._daylight_hours = self._preset.get_daylight_hours()

    # Save to the database.
    self._add_or_update_module_in_db()
    # Update the state.
    self.__update_state_from_module()

class ModuleInterface:
  """ Handles global tasks pertaining to the entire set of modules. """

  def __init__(self, serial, db, plant_presets):
    """
    Args:
      serial: This is the SerialTalker to use for communicating with modules.
      db: The database we are using.
      plant_presets: PresetManager instance containing the current loaded plant
                     presets.
    """
    logger.info("Initializing module interface...")

    # Keeps track of all the modules we currently have.
    self.__modules = set()
    # Serial interface to use for all module communication.
    self.__serial = serial
    # Database to store module settings.
    self.__module_collection = db.modules
    # Plant preset manager.
    self.__presets = plant_presets

    # Initialize the serial handler.
    self.__serial.add_message_handler(self.__common_handler)

  def __get_module_by_id(self, module_id):
    """ Gets a particular module by its ID.
    Args:
      module_id: The ID of the module.
    Returns:
      The module with that ID. """
    for module in self.__modules:
      if module.get_id() == module_id:
        return module

    # Could not find the module.
    raise KeyError("No module with ID %d." % (module_id))

  def __get_module_by_permanent_id(self, permanent_id):
    """ Gets a particular module by its permanent ID.
    Args:
      permanent_id: The permanent ID we are looking for.
    Returns:
      The module with that permanent ID. """
    for module in self.__modules:
      if module.get_permanent_id() == permanent_id:
        return module

    raise KeyError("No module with permanent ID %d." % (permanent_id))

  def __common_handler(self, message):
    """ Handles all relevant messages coming from the modules.
    Args:
      message: The message to handle. """

    if message.command == Message.ImAlive:
      # Handles incoming IMALIVE messages. It essentially runs the same
      # algorithm that the modules themselves run upon seeing this message, to
      # ensure that the IDs it sets for them here match the ones they choose for
      # themselves. The first field of this message is the module's currently
      # set permanent ID.
      self.add_module(int(message.fields[0]))

  def add_module(self, permanent_id, **kwargs):
    """ Adds a new module to the system. The module's permanent ID will also be
    automatically generated if it does not already exist.
    Args:
      permanent_id: The permanent ID of the module.
      Any other kwargs will be passed transparently to the module constructor. """
    logger.info("Discovered new module.")

    # The newest module always gets assigned the lowest ID, which is 3 in this
    # case since 0 is broadcast, 1 is us, and 2 is the BSC.
    new_module = Module(self.__module_collection, 3, permanent_id, **kwargs)

    # Increment all the other module IDs, since this is what they will do upon
    # receipt of the message.
    for module in self.__modules:
      module.increment_id()

    # Save the module.
    self.__modules.add(new_module)

    if not permanent_id:
      # We need to generate a permanent ID for this module.
      self.gen_permanent_id(new_module.get_id())

  def gen_permanent_id(self, module_id):
    """ Generates a new permanent ID for a module, and sends it to that module.
    Args:
      module_id: The (I2C) ID of the module. """
    module = self.__get_module_by_id(module_id)

    # Generate one.
    permanent_id = module.gen_permanent_id()
    logger.debug("Generated permanent ID for module %d: %d" % (module_id,
                                                               permanent_id))

    # Set it on the MCU.
    self.__serial.write_command(Message.SetPermanentId, module_id, permanent_id)

  def set_from_preset(self, permanent_id, preset_name):
    """ Sets module attributes from a preset.
    Args:
      permanent_id: The permanent_id of the module to set attributes for.
      preset_name: The name of the preset to use. """
    preset = self.__presets.get_preset(preset_name)
    module = self.__get_module_by_permanent_id(permanent_id)
    module.configure_from_preset(preset)

  def get_modules(self):
    """
    Returns:
      The set of modules currently attached. """
    return self.__modules

  def clear_modules(self):
    """ Clears all the currently managed modules. """
    self.__modules.clear()