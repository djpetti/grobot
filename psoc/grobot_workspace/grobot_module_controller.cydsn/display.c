#include "display.h"

#include <project.h>

void display_init() {
  // Start the UART.
  DISPLAY_UART_Start();
}