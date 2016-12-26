#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include <project.h>

#include "config.h"
#include "display.h"
#include "messaging.h"
#include "parser.h"
#include "sensors.h"

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

// Process a SETLED command.
// Args:
//  message: The message containing the command. It does nothing if the command
//           is not a SETLED command.
void _process_set_led(const struct Message *message) {
  if (strcmp(message->command, "SETLED")) {
    // Not a SETLED command.
    return;
  }
  
  // This command is used to set the target brightnesses of the LEDs in this
  // module.
  // Extract the brightnesses, which are in the fields section.
  const uint8_t red_brightness = atoi(parser_read_field(message, 0));
  const uint8_t white_brightness = atoi(parser_read_field(message, 1));
  const uint8_t blue_brightness = atoi(parser_read_field(message, 2));
  
  // Set the brightnesses.
  sensors_set_led_brightness(red_brightness, white_brightness, blue_brightness);
}

// Process a SETPMP command.
// Args:
//  message: The message containing the command. It does nothing if the command
//           is not a SETPMP command.
void _process_set_pump(const struct Message *message) {
  if (strcmp(message->command, "SETPMP")) {
    // Not a SETPMP command.
    return;
  }
  
  // This command is used to set whether the main pump is running or not.
  // Extract whether to run the pump.
  const uint8_t run_pump = atoi(parser_read_field(message, 0));
  // Set the pump.
  sensors_set_pump_running(run_pump);
}

// Processes a FNUTPH command.
// Args:
//  message: The message containing the command. It does nothing if the command
//           is not a FNUTPH command.
void _process_force_nutr_ph(const struct Message *message) {
  if (strcmp(message->command, "FNUTPH")) {
    // Not a FNUTPH command.
    return;
  }
  
  // This command is used to force the activation or deactivation of the
  // nutrient and PH pumps.
  // Extract whether to run the pumps.
  const uint8_t run_nutr = atoi(parser_read_field(message, 0));
  const uint8_t run_ph = atoi(parser_read_field(message, 1));
  
  // Set the pumps.
  sensors_force_nutr_ph(run_nutr, run_ph);
}

// Processes an ENSTAT command.
// Args:
//  message: The message containing the command. It does nothing if the command
//           is not an ENSTAT command.
void _process_en_status(const struct Message *message) {
  if (strcmp(message->command, "ENSTAT")) {
    // Not an ENSTAT command.
    return;
  }
  
  // This command is used to enable or disable the sending of serial status
  // messages from the sensors back to prime.
  // Extract whether or not to send status.
  const uint8_t send_status = atoi(parser_read_field(message, 0));
  
  // Set whether it's enabled.
  set_serial_status_enabled(send_status);
}

// Processes incoming messages.
// Args:
//  message: The incoming message to process.
void _process_message(struct Message message) {
#ifdef IS_BASE_CONTROLLER
  // If we're the base controller, we're in charge of forwarding messages
  // from the I2C bus to prime.
  if (message.dest == 1) {
    // Message for prime. Send it on the UART.
    messaging_forward_message(&message);
    return;
  }
#endif
  
  // One of these functions will handle it...
  _process_ping(&message);
  _process_set_id(&message);
  _process_set_led(&message);
  _process_set_pump(&message);
  _process_force_nutr_ph(&message);
  _process_en_status(&message);
}

int main()
{ 
    // Enable global interrupts.
    CyGlobalIntEnable;
  
    // Initialize messaging, with the callback.
    messaging_init(_process_message);
    
    // Start the display.
    display_init();
  
    // Register sensor interrupt.
    sensors_init();
    SENSOR_INT_StartEx(sensors_run_iteration);
    SENSOR_TIMER_Start();
    
    return 0;
}