#include "sensors.h"

#include <stdbool.h>
#include <stdint.h>
#include <project.h>

// Controls LED temperature by setting the fan speed.
void _control_led_temp() {
  // Read from the temperature sensors.
  
}

CY_ISR(sensors_run_iteration) {
  SENSOR_TIMER_ClearInterrupt(SENSOR_TIMER_INTR_MASK_TC);
}