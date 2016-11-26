#include <project.h>

#include "messaging.h"

int main()
{
    // Enable global interrupts.
    CyGlobalIntEnable;
  
    // Initialize messaging.
    messaging_init();
    
    // Read a message, and turn on the LED.
    struct Message message;
    messaging_get_message(&message);
    
    STATUS_LED_Write(1);
    
    return 0;
}