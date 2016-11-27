// Presents a unified API for passing messages between all controllers in the
// system.

#ifndef MODULE_CONTROLLER_MESSAGING_H_
#define MODULE_CONTROLLER_MESSAGING_H_
  
#include <stdbool.h>
#include <stdint.h>

#include "parser.h"
  
// Initialize the message passing interface. This will automatically perform
// the necessary handshakes and all to make sure that this controller can
// talk to the rest of the system.
// Returns:
//  True if initialization succeeds, false otherwise.
bool messaging_init();
// Performs a graceful exit from the system. Much of the time, this won't
// happen, because people will just remove modules from the system with no
// prior notice, but when it can be called, it's nice to do so.
//void messaging_exit();

// Sends a message.
// Args:
//  destination: The destination of the message. 0 is broadcast, 1 is prime,
//               and 2 is the base module controller.
//  command: The command associated with the message.
//  fields: The /-separated fields associated with the message.
void messaging_send_message(uint8_t destination, const char *command,
                            const char *fields);
// Waits for a new message to be ready, and then goes and processes it.
// Args:
//  message: The message to copy the new message into.
void messaging_get_message(struct Message *message);

// Sets a new controller ID. It will only set it if it hasn't been set
// before. Additionally, it will blink the new ID using the status LED for
// debugging purposes.
// Args:
//  id: The new controller id.
void messaging_set_controller_id(uint8_t id);
  
#endif // MODULE_CONTROLLER_MESSAGING_H_