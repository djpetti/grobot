#include "sensors.h"

#include <stdio.h>

#include <project.h>

#include "messaging.h"

// Channels to read LED temp data from.
static const uint8_t kRedLedTempChannel = 0;
static const uint8_t kWhiteLedTempChannel = 1;
static const uint16_t kBlueLedTempChannel = 2;

// Channels to read water data from.
static const uint16_t kWaterTempChannel = 3;

// Constants for linear mapping from raw ADC value temperature in C. We will
// multiply the value by 16 before dividing it by m.
static const int32_t kLedTempM = -429;
static const int32_t kLedTempB = 94;

// Constants for linear mapping from raw ADC value to water temperature in C.
// We will multiply the value by 16 before dividing it by m.
static const int32_t kWaterTempM = -429;
static const int32_t kWaterTempB = 94;

// Constant for linear mapping from temperature to fan speed. Nominally, we
// want the fan to turn on at 40C and reach full power by 70C.
static const int16_t kFanM = 8;
static const int16_t kFanB = -305;
// Bounds the maximum change in fan speed that we can make every cycle. This is
// in order to stop the fan from throttling up and down annoyingly.
static const int16_t kFanMaxChange = 3;

// The maximum PWM values for all the LEDs.
static const uint8_t kRedMaxPwm = 238;
static const uint8_t kWhiteMaxPwm = 242;
static const uint8_t kBlueMaxPwm = 242;

// How many cycles to leave in between status messages.
static const uint8_t kStatusPeriod = 10;

// The current PWM signals that we're sending to the LEDs.
static uint8_t g_red_pwm = 0;
static uint8_t g_white_pwm = 0;
static uint8_t g_blue_pwm = 0;

// The target PWMs for each LED.
static uint8_t g_red_target = 0;
static uint8_t g_white_target = 0;
static uint8_t g_blue_target = 0;

// Whether we are in a temperature fault condition.
static bool g_temp_fault = false;
// Whether the main pump is running or not.
static bool g_pump_running = false;
// Whether the nutrient and PH pumps are running or not.
static bool g_nutr_running = false;
static bool g_ph_running = false;

// It will send serial status back to prime only if this is enabled.
static bool g_serial_status = false;

// The last fan speed we output.
static int16_t g_fan_speed = 0;

// Send the status of the LED system back to Prime.
// Args:
//  red_temp: The temperature of the red LED.
//  white_temp: The temperature of the white LED.
//  blue_temp: The temperature of the blue LED.
//  fan_speed: The speed of the fan.
void _send_led_status(uint8_t red_temp, uint8_t white_temp, uint8_t blue_temp,
                      uint8_t fan_speed) {
  if (!g_serial_status) {
    // We're not sending the serial status.
    return;
  }
  
  // We probably are not going to want to send a status message every single
  // cycle.
  static uint8_t status_cycles = 0;
  if (++status_cycles <= kStatusPeriod) {
    return;
  }
  status_cycles = 0;
                        
  // Each attribute will be one field in the message.
  char fields[32];
  snprintf(fields, 32, "%u/%u/%u/%u/%u/%u/%u/%d", red_temp, white_temp,
           blue_temp, g_red_pwm, g_white_pwm, g_blue_pwm, fan_speed,
           g_temp_fault);
  
  messaging_send_message(1, "LEDSTS", fields);
}
                      
// Send the status of the water management system back to Prime.
// Args:
//  water_temp: The water temperature.
//  water_ec: The water conductivity.
//  water_ph: The water PH.
void _send_water_status(uint8_t water_temp, int8_t water_ec,
                        uint8_t water_ph) {
  if (!g_serial_status) {
    // We're not sending the serial status.
    return;
  }
  
  // We probably are not going to want to send a status message every single
  // cycle.
  static uint8_t status_cycles = 0;
  if (++status_cycles <= kStatusPeriod) {
    return;
  }
  status_cycles = 0;
  
  // Each attribute will be one field in the message.
  char fields[16];
  snprintf(fields, 16, "%u/%d/%u", water_temp, water_ec, water_ph);
  
  messaging_send_message(1, "WATSTS", fields);
}

// Controls LED temperature by setting the fan speed.
void _control_led_temp() {
  // Read from the temperature sensors.
  const uint16_t red_temp_raw = ADC_GetResult16(kRedLedTempChannel);
  const uint16_t white_temp_raw = ADC_GetResult16(kWhiteLedTempChannel);
  const uint16_t blue_temp_raw = ADC_GetResult16(kBlueLedTempChannel);
  
  // Convert to degrees C.
  const int32_t red_temp = (int32_t)(red_temp_raw << 4) / kLedTempM + kLedTempB;
  const int32_t white_temp = (int32_t)(white_temp_raw << 4) / 
                              kLedTempM + kLedTempB;
  const int32_t blue_temp = (int32_t)(blue_temp_raw << 4) /
                            kLedTempM + kLedTempB;
  
  // Set the fan speed based on the max.
  int16_t max_temp = red_temp;
  if (white_temp > max_temp) {
    max_temp = white_temp;
  }
  if (blue_temp > max_temp) {
    max_temp = blue_temp; 
  }
  
  const int16_t new_fan = max_temp * kFanM + kFanB;
  // Bound the rate of change.
  if (new_fan - g_fan_speed > kFanMaxChange) {
    g_fan_speed += kFanMaxChange;
  } else if (g_fan_speed - new_fan > kFanMaxChange) {
    g_fan_speed -= kFanMaxChange; 
  } else {
    g_fan_speed = new_fan; 
  }
  
  // Bound the fan speed intelligently.
  if (g_fan_speed < 0) {
    g_fan_speed = 0;
  } else if (g_fan_speed > 255) {
    g_fan_speed = 255; 
  }
  
  // Throttle down LED current if the LEDs are still getting really hot.
  g_temp_fault = false;
  if (red_temp > 80) {
    if (g_red_pwm < 25) {
      // We're sending very little current but still getting too hot. In this
      // case, we will force a complete shutdown.
      g_temp_fault = true; 
    } else {
      g_red_pwm -= 25; 
    }
  } else {
    // Use the target brightness.
    g_red_pwm = g_red_target;
  }
  
  if (white_temp > 80) {
    if (g_white_pwm < 25) {
      g_temp_fault = true; 
    } else {
      g_white_pwm -= 25;
    }
  } else {
    g_white_pwm = g_white_target; 
  }
  
  if (blue_temp > 80) {
    if (g_blue_pwm < 25) {
      g_temp_fault = true; 
    } else {
      g_blue_pwm -= 25; 
    }
  } else {
    g_blue_pwm = g_blue_target; 
  }
  
  // Bound PWMs to the maximum.
  if (g_red_pwm > kRedMaxPwm) {
    g_red_pwm = kRedMaxPwm; 
  }
  if (g_white_pwm > kWhiteMaxPwm) {
    g_white_pwm = kWhiteMaxPwm; 
  }
  if (g_blue_pwm > kBlueMaxPwm) {
    g_blue_pwm = kBlueMaxPwm; 
  }
  
  if (g_temp_fault) {
    // We need to perform an emergency shutdown of the LEDs.
    LED_MOSFET_Write(0);
    // Turn the fan up all the way.
    PWM_BLUE_FAN_WriteCompare2(255);
  } else {
    // Otherwise, white the PWMs like normal.
    LED_MOSFET_Write(1);
    // The drivers respond with full current when you send ground. It makes more
    // sense though for 255 to be full power, so we reverse the PWM compare
    // values when we set them.
    PWM_RED_WHITE_WriteCompare1(255 - g_red_pwm);
    PWM_RED_WHITE_WriteCompare2(255 - g_white_pwm);
    PWM_BLUE_FAN_WriteCompare1(255 - g_blue_pwm);
    PWM_BLUE_FAN_WriteCompare2(g_fan_speed);
  }
  
  // Send the LED status back to prime.
  _send_led_status(red_temp, white_temp, blue_temp, g_fan_speed);
}

// Gets the current water temperature and conductivity.
// Args:
//  temp: Will be set to the water temperature.
//  ec: Will be set to the water conductivity.
void _get_water_temp_ec(int32_t *temp, int32_t *ec) {
  // TODO (danielp): Implement conductivity as well.
  *ec = -1;
  
  const uint16_t water_temp_raw = ADC_GetResult16(kWaterTempChannel);
  *temp = (int32_t)(water_temp_raw << 4) / kWaterTempM + kWaterTempB;
  if (*temp < 20) {
    // Currently, we can't measure less than about 20 C very accurately, so
    // if the temperature is below this, we're not going to give a conductivity
    // reading.
    *ec = -1;
  }
}

void _control_water() {
  // Turn on the main pump accordingly.
  PUMP_MOSFET_Write(g_pump_running);
  
  // Turn on the nutrient and ph pumps if needed.
  NUTR_MOSFET_Write(g_nutr_running);
  PH_MOSFET_Write(g_ph_running);
  
  // Get the current temperature and conductivity.
  int32_t water_temp, water_ec;
  _get_water_temp_ec(&water_temp, &water_ec);
  
  // Send the water status back to prime.
  // TODO (danielp): Add water PH.
  _send_water_status(water_temp, water_ec, 7);
}

CY_ISR(sensors_run_iteration) {
  SENSOR_TIMER_ClearInterrupt(SENSOR_TIMER_INTR_MASK_TC);
  
  _control_led_temp();
  _control_water();
}

void sensors_init() {
  // Start the ADC.
  ADC_Start();
  ADC_StartConvert();
  
  // Initialize PWM outputs.
  PWM_RED_WHITE_Start();
  PWM_BLUE_FAN_Start();
  
  PWM_RED_WHITE_WriteCompare1(g_red_target);
  PWM_RED_WHITE_WriteCompare2(g_white_target);
  PWM_BLUE_FAN_WriteCompare1(g_blue_target);
  // Fan is initially off.
  PWM_BLUE_FAN_WriteCompare2(0);
  
  // Power up the drivers.
  LED_MOSFET_Write(g_serial_status);
  
  // Turn on the LED until someone enabled serial status. This is because
  // serial status generally gets enabled when prime is actively connected
  // to us, so the LED is a good way to quickly debug whether that connection
  // is working.
  STATUS_LED_Write(1);
}

void sensors_set_led_brightness(uint8_t red, uint8_t white, uint8_t blue) {
  // Set the targets.
  g_red_target = red;
  g_white_target = white;
  g_blue_target = blue;
}

void sensors_set_pump_running(bool running) {
  g_pump_running = running;
}

void sensors_force_nutr_ph(bool nutr_running, bool ph_running) {
  g_nutr_running = nutr_running;
  g_ph_running = ph_running;
}

void set_serial_status_enabled(bool enabled) {
  // Set the status LED appropriately.
  STATUS_LED_Write(!enabled);
  g_serial_status = enabled; 
}