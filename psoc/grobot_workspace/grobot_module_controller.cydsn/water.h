#ifndef MODULE_CONTROLLER_WATER_H_
#define MODULE_CONTROLLER_WATER_H_
  
#include <stdbool.h>
  
// Initialize water system.
void water_init();

// Enable or disable the sending of serial status back to prime.
// Args:
//  enabled: Whether or not serial status is enabled.
void water_set_serial_status_enabled(bool enabled);

// Sets whether the main pump is running or not.
// Args:
//  running: If true, the pump will run.
void water_set_pump_running(bool running);
// Normally, PH and nutrient pumps are activated automatically. This allows
// the user to override that and force them to run.
// Args:
//  nutr_running: Whether the nutrient pump is running.
//  ph_running: Whether the PH pump is running.
void water_force_nutr_ph(bool nutr_running, bool ph_running);

// Runs a single iteration of the water control loop.
void water_run_iteration();
  
#endif  // MODULE_CONTROLLER_WATER_H_