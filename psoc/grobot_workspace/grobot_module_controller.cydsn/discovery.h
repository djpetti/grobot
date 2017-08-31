#ifndef MODULE_CONTROLLER_DISCOVERY_H_
#define MODULE_CONTROLLER_DISCOVERY_H_

// Utilities related to module discovery. None of this will do much if it
// is running on the base system controller.
  
// Begins the discovery process for this module. This should be run first
// thing after the communications subsystems are initialized.
void discovery_init();
// Handles an IMALIVE message received from another module. This will
// automatically set the module's ID as necessary.
void discovery_handle_imalive();
  
#endif  // MODULE_CONTROLLER_DISCOVERY_H_