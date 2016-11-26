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

// Sends a message to a specific module in the stack.
// Args:
//  module: The module number to send it to. The modules are numbered from
//          bottom to top, starting at zero for the base system.
//  message: The message to send.
// Returns:
//  True if sending the message succeeded, false otherwise.
//bool messaging_send_message_to_module(uint8_t module, const char *message);
// Sends a message to the prime controller.
// Args:
//  message: The message to send.
// Returns:
//  True if sending the message succeeded, false otherwise.
//bool messaging_send_message_to_prime(const char *message);
// Waits for a new message to be ready, and then goes and processes it.
// Args:
//  message: The message to copy the new message into.
void messaging_get_message(struct Message *message);
  
#endif // MODULE_CONTROLLER_MESSAGING_H_