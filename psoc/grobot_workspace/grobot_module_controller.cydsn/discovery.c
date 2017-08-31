#include "discovery.h"

#include <stdbool.h>
#include <stdint.h>

#include "config.h"
#include "messaging.h"

// We need to keep track of our controller ID. If this is the base system, it
// will be 2, otherwise it will be determined during the discovery process.
#ifdef IS_BASE_CONTROLLER
static uint8_t g_controller_id = 2;
#else
static uint8_t g_controller_id = 3;
#endif

// Whether we have finished sending our discovery message.
static bool g_imalive_sent = false;
  
void discovery_init() {
#ifndef IS_BASE_CONTROLLER  
  // Send the IMALIVE command to alert other modules that we are online.
  messaging_send_message(0, "IMALIVE", "");
  
  // The way I2C works, after the above returns, the rest of the message must
  // get sent, and no other masters can grab the bus in the meantime. That means
  // that we're clear to start waiting for other IMALIVE messages at this point.
  g_imalive_sent = true;
#endif
  
  // Set the controller id.
  messaging_set_controller_id(g_controller_id);
}

void discovery_handle_imalive() {
#ifdef IS_BASE_CONTROLLER
  // Don't do anything for the base controller.
  return;
#endif
  
  if (!g_imalive_sent) {
    // Ignore them until we've sent our own.
    return;
  }
  
  // Increment the ID every time we receive one.
  ++g_controller_id;
  messaging_set_controller_id(g_controller_id);
}