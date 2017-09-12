import logging

from .. import serial_talker

from . import module_common


logger = logging.getLogger(__name__)


class GrowModule(module_common.ModuleCommon):
  """ Simulates a grow module controller. """

  def __init__(self, *args, permanent_id=0, **kwargs):
    """
    Args:
      permanent_id: Allows the user to specify a permanend ID for this module.
                    None is specified, it will act as if the permanent ID is not
                    set. """
    super().__init__(*args, **kwargs)

    # The ID of a Grow Module defaults to 3.
    self._id = 3
    self.__permanent_id = permanent_id
    # Whether we've written our discovery message yet.
    self.__sent_imalive = False

  def __handle_imalive(self, message):
    """ Handles ImAlive messages.
    Args:
      message: The message to handle. """
    if self.__sent_imalive:
      # Increment the ID when we see a new "module".
      self._id += 1
      logger.debug("Incrementing ID to %d" % (self._id))

  def __handle_setpermanentid(self, message):
    """ Handles SetPermanentId messages.
    Args:
      message: The message to handle. """
    # Reset the permanent ID.
    permanent_id = int(message.fields[0])
    logger.debug("Module %d: Setting permanent ID to %d." % \
                 (self._id, permanent_id))

    self.__permanent_id = permanent_id

  def __handle_getpermanentid(self, message):
    """ Handles GetPermanentId messages.
    Args:
      message: The message to handle. """
    # Send the permanent ID to the requester.
    logger.debug("%d: Permanent ID request from %d." % (self._id,
                                                        message.source))
    self._write_message(serial_talker.Message.GetPermanentId, message.source,
                        self.__permanent_id)

  def _handle_message(self, message):
    """ See superclass documentation. """
    super()._handle_message(message)

    if message.command == serial_talker.Message.ImAlive:
      self.__handle_imalive(message)
    if message.command == serial_talker.Message.SetPermanentId:
      self.__handle_setpermanentid(message)
    if message.command == serial_talker.Message.GetPermanentId:
      self.__handle_getpermanentid(message)

  def on_startup(self):
    """ See superclass documentation. """
    # Send the initial discovery message.
    self._write_message(serial_talker.Message.ImAlive, 0, self.__permanent_id)
    self.__sent_imalive = True
