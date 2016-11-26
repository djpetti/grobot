#include "parser.h"

void parser_message_init(struct Message *message) {
  // Initialize message fields.
  message->parser_state = READING_START;
  message->write_counter = 0;
  message->write_field = 0;
}

bool parser_parse_byte(struct Message *message, char byte) {
  // The standard format for a message is for it to start with a <,
  // and for single slashes to indicate the division between fields. Messages
  // are terminated with a >.
  switch (message->parser_state) {
    case READING_START:
      // We're looking for the leading <.
      if (byte == '<') {
        // We found the start.
        message->parser_state = READING_COMMAND;
      }
      break;
      
    case READING_COMMAND:
      // All bytes read now are part of the command, until we hit a slash.
      if (byte == '/') {
        // We're done reading the command.
        message->write_counter = 0;
        message->parser_state = READING_FIELD;
        break;
      }
      if (byte == '>') {
        // There are legal commands that have no fields.
        message->parser_state = DONE;
        break;
      }
      message->command[message->write_counter++] = byte;
      break;
      
    case READING_FIELD:
        // All bytes are part of this field, until we hit a control character.
        if (byte == '/') {
          // We hit the end of this field. 
          ++message->write_field;
          // We're going to put a null character at the end, just so we can
          // easily treat the field values as strings.
          message->fields[message->write_field * FIELD_LENGTH +
                          message->write_counter] = '\0';
          message->write_counter = 0;
          break;
        }
        if (byte == '>') {
          // We hit the end of the message.
          message->fields[message->write_field * FIELD_LENGTH +
                          message->write_counter] = '\0';
          message->parser_state = DONE;
          break;
        }
        message->fields[message->write_field * FIELD_LENGTH + 
                        message->write_counter++] = byte;
        break;
        
    case DONE:
        // Don't need to do anything.
        break;
  }
  
  if (message->parser_state == DONE) {
    // The message has been entirely parsed.
    return true;
  }
  return false;
}

const char *parser_read_field(const struct Message *message, uint8_t field) {
  return message->fields + field * FIELD_LENGTH;
}