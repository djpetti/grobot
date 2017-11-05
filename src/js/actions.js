// Namespace for this file.
actions = {};

// Updates the Redux state based on the backend state.
actions.UPDATE_BACKEND_STATE = 'UPDATE_BACKEND_STATE';
// Adds a new item to the action panel. This does everything except save the
// actual panel item into the state.
actions.ADD_PANEL_ITEM = 'ADD_PANEL_ITEM';
// Removes an item from the action panel. This does everything except remove the
// actual item from the state.
actions.REMOVE_PANEL_ITEM = 'REMOVE_PANEL_ITEM';
// Updates the list of panel items in the state. This
// is meant to be used by Sagas that catch the ADD_PANEL_ITEM or
// REMOVE_PANEL_ITEM actions, create or remove the panel item,
// and then save it into the state.
actions.UPDATE_PANEL_ITEM_LIST = 'UPDATE_PANEL_ITEM_LIST';
// Sets the core action panel object in the state.
actions.SET_ACTION_PANEL = 'SET_ACTION_PANEL';

/** Action creator that creates an UPDATE_BACKEND_STATE.
 * @param key The key for the part of the state we are updating. If it is an
 *            empty list, the top level of the state will be updated.
 * @param state The new backend state that you want to update.
 * @returns The created action.
 */
actions.updateBackendState = function(key, state) {
  return {type: actions.UPDATE_BACKEND_STATE, key, state};
}

/** Action creator that creates an ADD_PANEL_ITEM.
 * @param title The title of the item.
 * @param description The description of the item.
 * @param level The level of the item.
 * @param id A unique ID that will be used to identify this item.
 * @returns The created action.
 */
actions.addPanelItem = function(title, description, level, id) {
  return {type: actions.ADD_PANEL_ITEM, title, description, level, id};
}

/** Action creator that creates an UPDATE_PANEL_ITEM_LIST.
 * @param id A unique ID that will be used to identify this item.
 * @param item The actual DOM node containing the item, or null if we want to
 *             remove this item.
 * @returns The created action.
 */
actions.updatePanelItemList = function(id, item) {
  return {type: actions.UPDATE_PANEL_ITEM_LIST, id, item};
}

/** Action creator that creates a REMOVE_PANEL_ITEM.
 * @param id The unique ID of the item, specified at creation time.
 */
actions.removePanelItem = function(id) {
  return {type: actions.REMOVE_PANEL_ITEM, id};
}

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
    // Whether the MCU is currently active.
    mcu_alive: true,
    modules: {},
  },

  // Action panel data.
  actionPanel: {
    // Singleton action panel for the main view.
    actionPanel: null,
    // What items are currently visible in the action panel.
    items: {},

    // How many of each type of item there are.
    numError: 0,
    numWarning: 0,
    numNormal: 0,

    // The panel gives a "summary" message that has a level also.
    summaryLevel: 'normal',
  },
};

/** Reducer for backend state-related actions.
 * @private
 * @param state The current state.
 * @param action The action we want to modify the state with.
 * @returns The new state.
 */
actions.fromBackendReducer_ = function(state = {}, action) {
  switch (action.type) {
    case actions.UPDATE_BACKEND_STATE:
      // Make copy of the state.
      let newState = Object.assign({}, state);
      // Make a copy of the action key too since we also change that.
      const myKey = action.key.slice();

      const last_key = myKey.pop();
      let level = newState;
      console.log(myKey);
      for (i = 0; i < myKey.length; ++i) {
        let key = myKey[i];

        if (!(key in level)) {
          // Add a new level to the state.
          level[key] = {};
        }
        console.log(JSON.stringify(level));
        level = level[key];
      }

      // Set the state.
      if (!last_key) {
        // For some reason, JavaScript thinks that it's logical for popping from
        // an empty list to produce 'undefined'. In this case, if the key list
        // is empty, it means that we want to update the top-level state.
        newState = action.state;
      } else {
        level[last_key] = action.state;
      }

      console.log('Updated backend state: ' + JSON.stringify(newState));
      return newState;

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
  /** Simple helper function to update the panel summary level.
   * @param state The state to update.
   */
  let updateSummaryLevel = function(state) {
    // The summary level always gets set to the highest level of any item
    // in the panel.
    if (state.numError > 0) {
      state.summaryLevel = 'error';
    } else if (new_state.numWarning > 0) {
      state.summaryLevel = 'warning';
    } else {
      state.summaryLevel = 'normal';
    }
  };

  let new_state = Object.assign({}, state);
  let panel = null;

  switch (action.type) {
    case actions.SET_ACTION_PANEL:
      new_state.actionPanel = action.actionPanel;
      return new_state;

    case actions.ADD_PANEL_ITEM:
      switch (action.level) {
        case 'normal':
          ++new_state.numNormal;
          break;
        case 'warning':
          ++new_state.numWarning;
          break;
        case 'error':
          ++new_state.numError;
          break;
        default:
          console.error('Unknown action type: ' + action.level);
          return state;
      }

      updateSummaryLevel(new_state);

      return new_state;

    case actions.UPDATE_PANEL_ITEM_LIST:
      if (action.item) {
        // All we really have to do now is save the item by ID.
        new_state.items[action.id] = action.item;
      } else {
        // Delete the item.
        delete new_state.items[action.id];
      }

      return new_state;

    case actions.REMOVE_PANEL_ITEM:
      panel = state.actionPanel;
      if (!panel) {
        console.error('actionPanel not set in Redux state!');
        // We can't really update the state reasonably in this case.
        return state;
      }

      // Get the item with that ID.
      let to_remove = new_state.items[action.id];
      const level = to_remove.getLevel();

      // Decrement the level counters appropriately.
      switch (level) {
        case 'normal':
          --new_state.numNormal;
          break;
        case 'warning':
          --new_state.numWarning;
          break;
        case 'error':
          --new_state.numError;
          break;
        default:
          console.error('Unknown action type: ' + action.level);
          return state;
      }

      updateSummaryLevel(new_state);

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
