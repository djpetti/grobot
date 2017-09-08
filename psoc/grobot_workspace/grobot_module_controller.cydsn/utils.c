#include "utils.h"

void utils_moving_average(int32_t *total, int32_t *average, int32_t sample,
                          uint8_t window) {
  *total += sample;
  *total -= *average;
  *average = *total / window;
}