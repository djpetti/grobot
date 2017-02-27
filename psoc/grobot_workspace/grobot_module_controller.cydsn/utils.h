#ifndef MODULE_CONTROLLER_UTILS_H_
#define MODULE_CONTROLLER_UTILS_H_

#include <stdint.h>
  
// Some simplistic utility functions.
  
// Performs a moving average.
// Args:
//  total: The current total, which will be modified in-place.
//  average: The current average, which will be modified in-place.
//  sample: The new sample to incorporate.
//  window: How many samples the average encompasses.
void utils_moving_average(int32_t *total, int32_t *average, int32_t sample,
                          uint8_t window);
  
#endif  // MODULE_CONTROLLER_UTILS_H_