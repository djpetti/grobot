/** Set of predefined messages that can be displayed on the action panel. */

// Namespace for this file.
gbActionPanelMessages = {};

/** Message that gets displayed when we can't connect to the MCU. */
gbActionPanelMessages.mcuNotResponding =
  {
    title: 'Cannot connect to Base System Controller!',
    description: 'Your GroBot will not function until this is resolved.',
    level: 'error',
    id: 'mcuNotResponding',
  };

/** Message that gets displayed when there are no modules detected. */
gbActionPanelMessages.noModules =
  {
    title: 'No Grow Modules Detected',
    description: 'Make sure any grow modules are properly installed.',
    level: 'warning',
    id: 'noModules',
  };
