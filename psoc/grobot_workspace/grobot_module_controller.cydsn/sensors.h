#ifndef MODULE_CONTROLLER_SENSORS_H_
#define MODULE_CONTROLLER_SENSORS_H_

#include <stdbool.h>
#include <stdint.h>
  
#include <project.h>

// Initialize sensor stuff.
void sensors_init();
  
// Runs a single iteration of the sensor reader.
CY_ISR_PROTO(sensors_run_iteration);

// Enable or disable the sending of serial status back to prime.
// Args:
//  enabled: Whether or not serial status is enabled.
void set_serial_status_enabled(bool enabled);
// Sets new target brightnesses for the LEDs.
// Args:
//  red: Red brightness, from 0-255.
//  white: White brightness, from 0-255.
//  blue: Blue brightness, from 0-255.
void sensors_set_led_brightness(uint8_t red, uint8_t white, uint8_t blue);
// Sets whether the main pump is running or not.
// Args:
//  running: If true, the pump will run.
void sensors_set_pump_running(bool running);
// Normally, PH and nutrient pumps are activated automatically. This allows
// the user to override that and force them to run.
// Args:
//  nutr_running: Whether the nutrient pump is running.
//  ph_running: Whether the PH pump is running.
void sensors_force_nutr_ph(bool nutr_running, bool ph_running);

#endif // MODULE_CONTROLLER_SENSORS_H_