#include "water.h"

#include <stdint.h>
#include <stdio.h>

#include <project.h>

#include "messaging.h"
#include "utils.h"

// Channels to read water data from.
static const uint8_t kWaterTempChannel = 3;
static const uint8_t kWaterEcChannel = 5;

// Constants for linear mapping from raw ADC value to water temperature in C.
// We will multiply the value by 16 before dividing it by m.
static const int32_t kWaterTempM = -429;
static const int32_t kWaterTempB = 94;

// How many cycles to leave in between status messages.
static const uint8_t kStatusPeriod = 50;

// Window size for EC moving average.
static const uint8_t kEcAverageWindowSize = 10;

// The value of the resistor in the water EC circuit, in Ohms.
static const int32_t kEcResistor = 2200;
// The resistance of the digital pin + wire for the EC system. I couldn't find
// this documented anywhere, so I'm making a reasonable guess.
static const int32_t kEcPinResistance = 5;
// Cell constant for EC measurements, multiplied by 100. This is something that
// might benefit from calibration...
static const int32_t kEcCellConstant = 288;
// Temperature coefficient for temperature compensation. Apparently, this number
// is the standard for plant nutrients. Note that it is multiplied by 1000.
static const int32_t kTempCoefficient = 19;
// This is the standard PPM conversion constant for the US. Note that it is
// multiplied by 1000.
static const int32_t kPpmConversion = 500;

// It will send serial status back to prime only if this is enabled.
static bool g_serial_status = false;

// Whether the main pump is running or not.
static bool g_pump_running = false;
// Whether the nutrient and PH pumps are running or not.
static bool g_nutr_running = false;
static bool g_ph_running = false;

// How many analog readings we've taken so far for the EC sensor.
static uint8_t g_ec_readings = 0;
// The current raw value from the EC sensor.
static int32_t g_resistance_raw = -1;
// The total readings from the ec sensor over the past few cycles, used for
// calculating the average.
static int32_t g_resistance_total = -1;

// Updates the EC reading when new data comes in from the ADC.
CY_ISR(_update_ec) {
  if (g_ec_readings >= 2) {
    // We've already taken enough readings, so we don't need to do anything.
    return;
  }
  
  // Get the ADC value.
  const uint16_t ec_reading = ADC_GetResult16(kWaterEcChannel);
  ++g_ec_readings;
  
  if (g_ec_readings == 1) {
    // We're going to wait for one more, because we don't know if the power
    // pin had reached peak voltage yet when this was taken.
    return;
  } else if (g_ec_readings == 2) {
    // We've got the reading, turn off the power.
    WATER_EC_PWR_Write(0);
    
    if (ec_reading & 0xF000) {
      // We're just getting noise now, so throw it out.
      return;
    }
    
    if (g_resistance_raw < 0) {
      // This only happens when we don't have a reading yet. In this case,
      // the average will be way low, so we'll just take our first reading
      // as a reasonable guess.
      g_resistance_raw = ec_reading;
      // Make the total reasonable too.
      g_resistance_total = g_resistance_raw * kEcAverageWindowSize;
      return;
    }
    
    // Now we have an actual reading. Add it to the average.
    utils_moving_average(&g_resistance_total, &g_resistance_raw, ec_reading,
                         kEcAverageWindowSize);
  }
}

// Send the status of the water management system back to Prime.
// Args:
//  water_temp: The water temperature.
//  water_ec: The water conductivity.
//  water_ph: The water PH.
void _send_water_status(uint8_t water_temp, int16_t water_ec,
                        uint8_t water_ph) {
  if (!g_serial_status) {
    // We're not sending the serial status.
    return;
  }
  
  // Each attribute will be one field in the message.
  char fields[16];
  snprintf(fields, 16, "%u/%d/%u", water_temp, water_ec, water_ph);
  
  // Since this is just a status message, we don't have to block everything
  // waiting for the send to succeed.
  messaging_send_message(1, "WATSTS", fields);
}
                        
// Gets the current water temperature and conductivity.
// Args:
//  temp: Will be set to the water temperature.
//  ppm: The dissolved solids concentration in PPM.
void _get_water_temp_ec(int32_t *temp, int32_t *ppm) {
  const uint16_t water_temp_raw = ADC_GetResult16(kWaterTempChannel);
  *temp = (int32_t)(water_temp_raw << 4) / kWaterTempM + kWaterTempB;
  
  // Briefly turn on power to the EC sensor. It will be turned off by the ISR
  // after we get the reading.
  WATER_EC_PWR_Write(1);
  // Resetting this flag will tell the ISR to start taking a reading.
  g_ec_readings = 0;
  
  // First, convert raw ADC reading to a voltage.
  // Because our ADC ranges from 0 to 2048, we can divide with a convenient
  // shift operation. The 2500 comes from the fact that out ADC reference is
  // 2500 mV.
  const int32_t v_drop = (g_resistance_raw * 2500) >> 11;
  // Use voltage drop to calculate the resistance of the water in Ohms.
  // 5000 is Vcc, in mV.
  int32_t water_resistance = v_drop * kEcResistor / (5000 - v_drop);
  // Compensate for the digital pin resistance.
  water_resistance -= kEcPinResistance;
  // Compute the EC from the resistance. (This will be 1000X)
  const int32_t water_ec = 100000000 / (water_resistance * kEcCellConstant);
  
  // Compensate for temperature. (This will also be 1000X)
  const int32_t ec_at_25 = water_ec * 1000 /
                           (1000 + kTempCoefficient * (*temp - 25));
  // Calculate PPM.
  *ppm = ec_at_25 * kPpmConversion / 1000;
}

void water_run_iteration() {
  // Turn on the main pump accordingly.
  PUMP_MOSFET_Write(g_pump_running);
  
  // Turn on the nutrient and ph pumps if needed.
  NUTR_MOSFET_Write(g_nutr_running);
  PH_MOSFET_Write(g_ph_running);
  
  // Water temp and EC are not something that must be computed at high
  // frequency.
  static uint8_t status_cycles = 0;
  if (++status_cycles <= kStatusPeriod) {
    return;
  }
  status_cycles = 0;
  
  // Get the current temperature and conductivity. 
  int32_t water_temp, water_ec;
  _get_water_temp_ec(&water_temp, &water_ec);
  
  // Send the water status back to prime.
  // TODO (danielp): Add water PH.
  _send_water_status(water_temp, water_ec, 7);
}

void water_set_serial_status_enabled(bool enabled) {
  g_serial_status = enabled;
}

void water_set_pump_running(bool running) {
  g_pump_running = running;
}

void water_init() {
  ADC_IRQ_Enable();
  ADC_EOC_INT_StartEx(_update_ec);
}

void water_force_nutr_ph(bool nutr_running, bool ph_running) {
  g_nutr_running = nutr_running;
  g_ph_running = ph_running;
}