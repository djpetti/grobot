// Namespace for this file.
actions = {};

// Updates the Redux state based on the backend state.
actions.UPDATE_BACKEND_STATE = 'UPDATE_BACKEND_STATE';
// Adds a new item to the action panel.
actions.ADD_PANEL_ITEM = 'ADD_PANEL_ITEM';
// Sets the core action panel object in the state.
actions.SET_ACTION_PANEL = 'SET_ACTION_PANEL';

/** Action creator that creates an UPDATE_BACKEND_STATE.
 * @param state The new backend state that you want to update.
 * @returns The created action.
 */
actions.updateBackendState = function(state) {
  return {type: actions.UPDATE_BACKEND_STATE, state};
};

/** Action creator that creates an ADD_PANEL_ITEM.
 * @param title The title of the item.
 * @param description The description of the item.
 * @param level The level of the item.
 * @returns The created action.
 */
actions.addPanelItem = function(title, description, level) {
  return {type: actions.ADD_PANEL_ITEM, title, description, level};
};

/** Action creator that creates a SET_ACTION_PANEL.
 * @param actionPanel The action panel node.
 * @returns The created action.
 */
actions.setActionPanel = function(actionPanel) {
  return {type: actions.SET_ACTION_PANEL, actionPanel};
}

/** The initial state of the application. */
actions.initialState = {
  // State from the backend that's synchronized to us.
  fromBackend: {
    // Whether the error modal is currently open.
    errorModalOpened: false,
  },

  // Action panel data.
  actionPanel: {
    // Singleton action panel for the main view.
    actionPanel: null,
    // What items are currently visible in the action panel.
    error: [],
    warning: [],
    normal: [],
  },
};

/** Reducer for the error modal status.
 * @private
 * @param state The current state.
 * @param action The action we want to modify the state with.
 * @returns The new state.
 */
actions.fromBackendReducer_ = function(state = {}, action) {
  switch (action.type) {
    case actions.UPDATE_BACKEND_STATE:
      let showErrorModal = !action.state.mcu_alive;
      return Object.assign({}, state, {errorModalOpened: showErrorModal});

    default:
      return state;
  }
};

/** Reducer for the action panel.
 * @private
 * @param state The current state.
 * @param action The action we want to modify the state with.
 * @returns The new state.
 */
actions.actionPanelReducer_ = function(state = {}, action) {
  switch (action.type) {
    case actions.SET_ACTION_PANEL:
      return Object.assign({}, state, {actionPanel: action.actionPanel});

    case actions.ADD_PANEL_ITEM:
      var new_state = Object.assign({}, state)

      // Add the actual item to the DOM.
      let panel = state.actionPanel;
      if (!panel) {
        console.error('actionPanel not set in Redux state!');
        // We can't really update the state reasonably in this case.
        return state;
      }
      let node = panel.addItem(action.title, action.description, action.level);

      switch (action.level) {
        case 'normal':
          new_state.error.push(node);
        case 'warning':
          new_state.warning.push(node);
        case 'error':
          new_state.error.push(node);
      }

      return new_state;

    default:
      return state
  }
}

/** Reducer for the GroBot app
* @param state The current state.
* @param action The action we want to modify the state with.
* @returns The new state. */
actions.grobotAppReducer = function(state = actions.initialState, action) {
  // Handle our actions.
  return {
    fromBackend: actions.fromBackendReducer_(state.fromBackend, action),
    actionPanel: actions.actionPanelReducer_(state.actionPanel, action),
  };
};
