// Simple utility for parsing messages from the message-passing system.

#include <stdbool.h>
#include <stdint.h>

// Maximum length of a command ID.
#define COMMAND_LENGTH 8
// Maximum number of command fields.
#define NUM_FIELDS 3
// Maximum length of command fields.
#define FIELD_LENGTH 32

// Keeps track of the parser state.
enum State {
  // We're looking for the start indicator.
  READING_START,
  // We're reading the command.
  READING_COMMAND,
  // We're reading the fields.
  READING_FIELD,
  // Done reading the message.
  DONE
};

// Represents a parsed message.
struct Message {
  // The command associated with the message.
  char command[COMMAND_LENGTH];
  // The fields associated with the message.
  char fields[NUM_FIELDS * FIELD_LENGTH];
  
  // Internal parameter that keeps track of parser state.
  enum State parser_state;
  // This is just a helper counter to we can write bytes sequentially.
  uint8_t write_counter;
  // This is another counter so we can write to the correct field.
  uint8_t write_field;
};

// Initialize a new message. This should be called before parser_parse_byte.
// Args:
//  message: The message to initialize.
void parser_message_init(struct Message *message);
// Parses a new byte that was read from the input.
// Args:
//  message: The message to modify.
//  byte: The byte to parse.
// Returns:
//  True if the message is now complete, false if more still has to be read.
bool parser_parse_byte(struct Message *message, char byte);

// Accesses the value of a particular field in a message object.
// Args:
//  message: The message to use.
//  field: The field number to get.
// Returns:
//  A pointer to the value of the field. It will be at most FIELD_LENGTH in 
//  size.
const char *parser_read_field(const struct Message *message, uint8_t field);