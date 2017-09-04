from .. import serial_talker

from . import module_common


class BaseModule(module_common.ModuleCommon):
  """ Simulates the base system controller. """

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # The ID of the base module is always 2.
    self._id = 2

  def on_startup(self):
    """ See superclass documentation. """
    # Nothing needs to be done by the base module during startup.
    pass
