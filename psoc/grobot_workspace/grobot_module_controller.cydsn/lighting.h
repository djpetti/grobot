#ifndef MODULE_CONTROLLER_LIGHTING_H_
#define MODULE_CONTROLLER_LIGHTING_H_

#include <stdbool.h>
#include <stdint.h>
  
#include <project.h>

// Initialize lighting stuff.
void lighting_init();

// Enable or disable the sending of serial status back to prime.
// Args:
//  enabled: Whether or not serial status is enabled.
void lighting_set_serial_status_enabled(bool enabled);

// Sets new target brightnesses for the LEDs.
// Args:
//  red: Red brightness, from 0-255.
//  white: White brightness, from 0-255.
//  blue: Blue brightness, from 0-255.
void lighting_set_led_brightness(uint8_t red, uint8_t white, uint8_t blue);

// Runs a single iteration of the lighting control loop.
void lighting_run_iteration();

#endif // MODULE_CONTROLLER_LIGHTING_H_