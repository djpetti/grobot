#ifndef MODULE_CONTROLLER_SENSORS_H_
#define MODULE_CONTROLLER_SENSORS_H_

#include <stdint.h>
  
#include <project.h>

// Initialize sensor stuff.
void sensors_init();
  
// Runs a single iteration of the sensor reader.
CY_ISR_PROTO(sensors_run_iteration);

// Sets new target brightnesses for the LEDs.
// Args:
//  red: Red brightness, from 0-255.
//  white: White brightness, from 0-255.
//  blue: Blue brightness, from 0-255.
void sensors_set_led_brightness(uint8_t red, uint8_t white, uint8_t blue);

#endif // MODULE_CONTROLLER_SENSORS_H_