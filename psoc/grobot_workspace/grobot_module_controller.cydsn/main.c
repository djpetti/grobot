#include <stdbool.h>
#include <string.h>

#include <project.h>

#include "messaging.h"

// Process a PING command.
// Args:
//  message: The message containing the command. It does nothing if the command
//           is not a PING command.
void _process_ping(const struct Message *message) {
  if (strcmp(message->command, "PING")) {
    // Not a PING command.
    return;
  }
  if (!strcmp(message->fields, "ack")) {
    // If we're just receiving an ack, we don't want to send anything back.
    return;
  }
  
  // In this case, we have to send back a response. We can figure out who
  // to send it to from the source.
  messaging_send_message(message->source, "PING", "ack");
}

// Process a SETID command.
// Args:
//  message: The message containing the command. It does nothing if the command
//           is not a SETID command.
void _process_set_id(const struct Message *message) {
  if (strcmp(message->command, "SETID")) {
    // Not a SETID command.
    return;
  }
  
  // This command is used so prime can set the controller ID of a module
  // controller. That means that when we receive one, we need to reset the ID.
  if (message->source != 1) {
    // We don't want to let anyone except prime do this.
    return;
  }
  // Extract the actual ID, which is the singular field.
  uint8_t id = message->fields[0] - 48;
  // Now, write the new ID.
  messaging_set_controller_id(id);
}

// Processes incoming messages.
// Args:
//  message: The incoming message to process.
void _process_message(const struct Message *message) {
  // One of these functions will handle it...
  _process_ping(message);
  _process_set_id(message);
}

int main()
{
    // Enable global interrupts.
    CyGlobalIntEnable;
  
    // Initialize messaging.
    messaging_init();
    
    // Read a message, and turn on the LED.
    struct Message message;
    while (true) {
      messaging_get_message(&message);
      
      _process_message(&message);
    }
    
    return 0;
}