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

/** Gets the Redux store for the app, or initializes a new one if it is not
 * created yet.
 * @returns The Redux store.
 */
main.getReduxStore = function() {
  if (!main.reduxStore) {
    // Create a new one.
    main.reduxStore = Redux.createStore(function(state, action) {
      return state;
    });
  }

  return main.reduxStore;
};

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
