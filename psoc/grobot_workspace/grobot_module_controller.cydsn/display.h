// Utility for talking to the LCD display.

#ifndef MODULE_CONTROLLER_DISPLAY_H_
#define MODULE_CONTROLLER_DISPLAY_H_
  
// Initialize the display. By default, it will just write "GroBot" to it.
void display_init();

// Clear the display.
void display_clear();
// Write something to the display.
// Args:
//  write: The string to write.
void display_write(const char *write);
  
#endif // MODULE_CONTROLLER_DISPLAY_H_
