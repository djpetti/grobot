// Namespace for everything in this file.
main = {};

/** @private
 * The Redux store for the app.
 */
main.reduxStore = null;
/** @private
 * The Redux behavior for Polymer.
 */
main.reduxBehavior = null;
/** @private
 * Saga middleware.
 */
main.sagaMiddleware = null;

/** @private
 * Initializes Redux, with the appropriate Saga middleware. This should be
 * called exactly once.
 */
main.initRedux_ = function() {
  console.log("Creating Redux store.")

  main.sagaMiddleware = ReduxSaga.default();
  let saga = Redux.applyMiddleware(main.sagaMiddleware);
  main.reduxStore = Redux.createStore(actions.grobotAppReducer, saga);
}

/** Gets the Redux store for the app, or initializes a new one if it is not
 * created yet.
 * @returns The Redux store.
 */
main.getReduxStore = function() {
  if (!main.reduxStore) {
    // Redux is not yet initialized.
    main.initRedux_();
  }

  return main.reduxStore;
};

/** Gets the Saga middleware for the app, or initializes it if it is not yet
 * initialized.
 * @returns The Saga middleware.
 */
main.getSagaMiddleware = function() {
  if (!main.sagaMiddleware) {
    // Redux is not yet initialized.
    main.initRedux_();
  }

  return main.sagaMiddleware;
}

/** Gets the Redux behavior for the app, or initializes a new one if it is not
 * created yet.
 * @returns The Redux behavior.
 */
main.getReduxBehavior = function() {
  if (!main.reduxBehavior) {
    // Create a new one.
    main.reduxBehavior = PolymerRedux(main.getReduxStore());
  }

  return main.reduxBehavior;
};

/** Initializes everything when the main view is loaded.
 */
main.initMain = function() {
  // Start running websocket client.
  let backend = new websockets.Backend();
}
