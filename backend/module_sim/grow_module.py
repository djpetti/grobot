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

  def on_startup(self):
    """ See superclass documentation. """
    # Send the initial discovery message.
    self._write_message(serial_talker.Message.ImAlive, 0, self.__permanent_id)
    self.__sent_imalive = True

  def _handle_message(self, message):
    """ See superclass documentation. """
    super()._handle_message(message)

    if message.command == serial_talker.Message.ImAlive:
      if self.__sent_imalive:
        # Increment the ID when we see a new "module".
        self._id += 1
        logger.debug("Incrementing ID to %d" % (self._id))
