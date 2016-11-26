#include "messaging.h"

#include <string.h>

#include <project.h>

#include "config.h"

// Size of the slave receiving data buffer.
#define RECV_BUFFER_SIZE 128
// Size of the slave sending data buffer.
#define SEND_BUFFER_SIZE 128

// Array that maps an I2C address to each module number.
uint8_t g_module_addresses[255];

// Stores the most recently partially received message from acting as a
// master and a slave, and for the UART.
struct Message g_master_message_part;
struct Message g_slave_message_part;
struct Message g_uart_message_part;
// Stores the most recently received message from any source.
// TODO (danielp): Make this an actual queue.
struct Message g_newest_message;
// Flag that is set whenever g_newest_message is updated.
bool g_new_message = false;

// The I2C write buffer to use when operating in slave mode.
uint8_t g_slave_recv_buffer[RECV_BUFFER_SIZE];
// The I2C read buffer to use when operating in slave mode.
uint8_t g_slave_send_buffer[SEND_BUFFER_SIZE];

// Procedures for handling a byte that are common across the master, slave,
// and UART interfaces.
// Args:
//  message_part: The message to modify.
//  byte: The new received byte.
void _handle_byte_common(struct Message *message_part, uint8_t byte) {
  // Parse the byte.
  if (parser_parse_byte(message_part, byte)) {
    // We have a complete message.
    memcpy(&g_newest_message, message_part, sizeof(*message_part));
    g_new_message = true;
    parser_message_init(message_part);
  }
}

// Handles data being sent from a slave to us.
void _handle_slave_response() {
  // Read the next byte of data sent to us.
  uint32_t byte = STACK_I2C_I2CMasterReadByte(STACK_I2C_I2C_ACK_DATA);
  if (byte & 0xFF000000) {
    // According to the docs, if the MSB is 1, that means that an error
    // occurred. If this happens, we can't do all that much besides drop the
    // message.
    parser_message_init(&g_master_message_part);
    return;
  }
  
  _handle_byte_common(&g_master_message_part, byte);
}

// Handles data being sent from a master to us.
void _handle_master_response() {
  // Read the next bytes of data sent to us.
  uint8_t bytes_to_read = STACK_I2C_I2CSlaveGetWriteBufSize();
  uint8_t i;
  for (i = 0; i < bytes_to_read; ++i) {
    uint8_t byte = g_slave_recv_buffer[i]; 
    _handle_byte_common(&g_slave_message_part, byte);
  }
  
  // Clear the buffer when we're done.
  STACK_I2C_I2CSlaveClearWriteBuf();
}

#ifdef IS_BASE_CONTROLLER
// Handle a response from the UART.
CY_ISR(_handle_uart_response) {
  // Clear the interrupt and get the status.
  uint8_t status = PRIME_UART_ReadRxStatus();
  if ((status & PRIME_UART_RX_STS_PAR_ERROR) ||
      (status & PRIME_UART_RX_STS_STOP_ERROR) ||
      (status & PRIME_UART_RX_STS_OVERRUN)) {
    // An error occurred. The current message is most likely corrupted now,
    // so we're going to drop it.
    parser_message_init(&g_uart_message_part);
    return;
  }
      
  // Read the byte. (We should never get an error condition, because we
  // already checked for that with the status).
  char byte = PRIME_UART_GetChar();
  _handle_byte_common(&g_uart_message_part, byte);
}
#endif

// Interrupt handler for the I2C subsystem.
CY_ISR(_handle_i2c) {
  // Get the cause of the interrupt and take appropriate action.
  uint32_t cause = STACK_I2C_GetInterruptCause();
  if (cause & STACK_I2C_INTR_CAUSE_RX) {
    if (cause & STACK_I2C_INTR_CAUSE_SLAVE) {
      // We got a reply from a slave. Handle it accordingly.
      _handle_slave_response();
    } else if (cause & STACK_I2C_INTR_CAUSE_MASTER) {
      // We got a reply from a master. Handle it accordingly.
      _handle_master_response();
    }
  }
}

bool messaging_init() {
#ifdef IS_BASE_CONTROLLER
  parser_message_init(&g_uart_message_part);
  
  // We should have a direct UART connection to Prime. Make sure we can talk
  // on that.
  PRIME_UART_Start();
  
  // This message should be immediately acknowledged.
  PRIME_UART_PutString("<PING>");
  
  // Wait for acknowledgement.
  const char *kExpected = "<PING/prime>";
  char received[strlen(kExpected) + 1];
  // Terminating null.
  received[strlen(kExpected)] = '\0';
  uint8_t i;
  for (i = 0; i < strlen(kExpected); ++i) {
    received[i] = 0;
    while (!received[i]) {
      received[i] = PRIME_UART_GetChar();
    }
  }

  if (strcmp(received, kExpected)) {
    // We didn't receive the ack value we expected.
    return false;
  }
  
  // Enable the interrupt.
  PRIME_UART_RECV_INT_StartEx(_handle_uart_response);
#endif

  parser_message_init(&g_master_message_part);
  parser_message_init(&g_slave_message_part);

  // Initialize the I2C layer so we can talk to other modules.
  STACK_I2C_Start();
  // Initialize the slave buffers.
  STACK_I2C_I2CSlaveInitWriteBuf(g_slave_recv_buffer, RECV_BUFFER_SIZE); 
  STACK_I2C_I2CSlaveInitReadBuf(g_slave_send_buffer, SEND_BUFFER_SIZE);
  // Set the interrupt handler.
  STACK_I2C_SetCustomInterruptHandler(_handle_i2c);
  
  // In order to set our address in a way that does not conflict, we're first
  // going to send out a ping on the general call address, so we can get
  // everyone else's address.
  const char *kPing = "<PING>";
  STACK_I2C_I2CMasterWriteBuf(0x00, (uint8_t *)kPing, strlen(kPing) + 1,
                              STACK_I2C_I2C_MODE_COMPLETE_XFER);
  
  // Responses to the ping will be handled by the ISR, and the address array
  // will be updated accordingly, so we can just go on for now.
  return true;
}

void messaging_get_message(struct Message *message) {
  // Get the newest message.
  while (!g_new_message);
  memcpy(message, &g_newest_message, sizeof(g_newest_message));
  g_new_message = false;
}