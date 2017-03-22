// Namespace for this file.
actions = {};

// Updates the Redux state based on the backend state.
actions.UPDATE_BACKEND_STATE = 'UPDATE_BACKEND_STATE';

/** Action creator that creates an UPDATE_BACKEND_STATE.
 * @param state The new backend state that you want to update.
 * @returns The created action.
 */
actions.updateBackendState = function(state) {
  return {type: actions.UPDATE_BACKEND_STATE, state}
};

/** The initial state of the application. */
actions.initialState = {
  // Whether the error modal is currently open.
  errorModalOpened: false,
};

/** Reducer for the GroBot app
* @param state The current state.
* @param action The action we want to modify the state with.
* @returns The new state. */
actions.grobotAppReducer = function(state = actions.initialState, action) {
  // Handle our actions.
  switch (action.type) {
    case actions.UPDATE_BACKEND_STATE:
      var showErrorModal = !action.state['mcu_alive'];
      return Object.assign({}, state, {errorModalOpened: showErrorModal});

    default:
      return state;
  }

  return state;
};
