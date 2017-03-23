// Namespace for this file.
websockets = {};

// The URL to connect to the backend on.
// TODO (danielp): Make this more flexible, instead of hard-coding the URL.
websockets.BACKEND_URL = 'ws://127.0.0.1:8080/app_socket'

/** Represents a connection to the backend, via a websocket. */
websockets.Backend = class {
  constructor() {
    this.socket = new WebSocket(websockets.BACKEND_URL);

    // Register handlers.
    var outer_this = this;
    this.socket.onopen = function() {
      outer_this.updateBackendState_();
    };
    this.socket.onmessage = function(event) {
      outer_this.receiveMessage_(event);
    };
  }

  /** Sends a request to the server for the initial state, and updates the Redux
   * state accordingly.
   @private */
  updateBackendState_() {
    // Send a state request message to the backend.
    var message = {type: 'state'};
    this.socket.send(JSON.stringify(message));
  }

  /** Processes an incoming message from the server.
   @private
   @param event The event object passed to us by the websocket interface. */
  receiveMessage_(event) {
    let message = JSON.parse(event.data);

    switch (message.type) {
      case 'state':
        // There was a state change on the server. Reflect it accordingly in
        // Redux.
        let store = main.getReduxStore();
        store.dispatch(actions.updateBackendState(message.state));
        break;

      default:
        // Not a known message type.
        console.log('Not handling unknown message type: ' + message.type)
    };
  }
};
