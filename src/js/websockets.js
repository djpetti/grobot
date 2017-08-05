// Namespace for this file.
websockets = {};

// The URL to connect to the backend on.
// TODO (danielp): Make this more flexible, instead of hard-coding the URL.
websockets.BACKEND_URL = 'ws://127.0.0.1:8080/app_socket'

/** Represents a connection to the backend, via a websocket. */
websockets.Backend = class {
  /**
   @param noConnect Will not connect immediately to the socket when true. */
  constructor(noConnect = false) {
    if (!noConnect) {
      // Connect to the socket.
      this.connect();
    }
  }

  /** Connect to the websocket. This is normally done automatically in the
   * constructor unless noConnect is specified. */
  connect() {
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
    this.processMessage_(message);
  }

  /** Processes a received message, and updates things accordingly.
   @private
   @param message The JSON message that was received. */
  processMessage_(message) {
    switch (message.type) {
      case 'state':
        // There was a state change on the server. Reflect it accordingly in
        // Redux.
        let store = main.getReduxStore();
        store.dispatch(actions.updateBackendState(message.state));
        break;

      default:
        // Not a known message type.
        throw new TypeError(
            'Not handling unknown message type: ' + message.type);
        return;
    };

    // Perform any necessary updates to other components after the state change.
    this.updateAfterStateChange_();
  }

  /** Updates any components that need to be updated after the state changes.
   @private */
  updateAfterStateChange_() {
    let store = main.getReduxStore();
    const backendState = store.getState().fromBackend;

    // Update the action panel.
    if (!backendState.mcuAlive) {
      // If the MCU is dead, we want to show a message on the action panel about
      // it.
      const message = gbActionPanelMessages.mcuNotResponding;
      const deadAction = actions.addPanelItem(message.title,
                                              message.description,
                                              message.level,
                                              message.id);
      store.dispatch(deadAction);
    }
  }
};
