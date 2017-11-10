// Namespace for this file.
gbActionPanel = {};

/** Creates the element. */
gbActionPanel.create = function() {
  console.log('Creating action panel.');
  Polymer({
    is: 'gb-action-panel',

    ready: gbActionPanel.ready_,

    addItem: gbActionPanel.addItem_,
    removeItem: gbActionPanel.removeItem_,
    updatePanelTop: gbActionPanel.updatePanelTop_,
  });
};

/** Runs on creation for the action panel.
 * @private
 */
gbActionPanel.ready_ = function() {
  console.log('Starting Sagas.');

  // Start running sagas.
  let saga = main.getSagaMiddleware();
  saga.run(gbActionPanel.sagas.addSagaWaiter_);
  saga.run(gbActionPanel.sagas.removeSagaWaiter_);
  saga.run(gbActionPanel.sagas.updateBackendStateSagaWaiter_);

  // Register the instance.
  let store = main.getReduxStore();
  store.dispatch(actions.setActionPanel(this));
};

/** Adds a new item to the action panel.
 * @private
 * @param title The title of the item.
 * @param description The description of the item.
 * @param level The level of the item. Must by a string in
 *              "normal", "warning", or "error".
 * @return The DOM node of the added item.
 */
gbActionPanel.addItem_ = function(title, description, level) {
  // First, create a new child item.
  let item = document.createElement('gb-action-panel-item');

  // Configure the item.
  item.setTitle(title);
  item.setDescription(description);
  item.setLevel(level);

  // Add the child node, but make sure that it comes in the correct position. We
  // can examine the Redux state to figure out how far down it should go.
  let store = main.getReduxStore();
  const state = store.getState();

  // Error items should always go at the top, warning items directly below, and
  // normal items at the bottom.
  let nodeAfter = null;
  let localDom = Polymer.dom(this);
  if (localDom.children.length) {
    // If we have no items, we can just append.
    if (level == 'error') {
      // It can go at the top.
      nodeAfter = localDom.children[0];
    }
    if (level == 'warning') {
      const errorLength = state.actionPanel.numError;

      if (!errorLength) {
        // No errors.
        nodeAfter = localDom.children[0];
      } else {
        // Add it after the errors.
        nodeBefore = localDom.children[errorLength - 1];
        // We do it this way so it handles the "we only have errors" case
        // correctly.
        nodeAfter = Polymer.dom(nodeBefore).nextSibling;
      }
    }
    // If it's normal, we can just add it at the end.
  }

  // Insert it before the proper child.
  Polymer.dom(this).insertBefore(item, nodeAfter);

  return item;
};

/** Removes an item from the action panel.
 * @private
 * @param item The node to remove from the panel. */
gbActionPanel.removeItem_ = function(item) {
  let panel = Polymer.dom(this);
  panel.removeChild(item);
};

/** Updates the messages at the top of the action panel based on what items are
 * present.
 * @param panelState The action panel part of the state.
 * @private */
gbActionPanel.updatePanelTop_ = function(panelState) {
  // Update the summary based on the current state.
  switch (panelState.summaryLevel) {
    case 'error':
      // We have errors.
      this.$.statusText.textContent = 'Action required!';
      this.$.description.textContent = 'Uh oh! It looks like there are' +
                                          ' some problems with your GroBot.';

      // Change the icon to an error icon.
      this.$.statusIcon.src = gbActionPanelItem.ICON_URLS['error'];
      break;

    case 'warning':
      // We have warnings.
      this.$.statusText.textContent = 'Action suggested.';
      this.$.description.textContent = 'Your GroBot may need some maintenence.' +
                                       ' See below for details.';

      // Change the icon to a warning icon.
      this.$.statusIcon.src = gbActionPanelItem.ICON_URLS['warning'];
      break;

    case 'normal':
      // Normal status.
      this.$.statusText.textContent = 'All systems nominal.';
      this.$.description.textContent = 'Your GroBot is functioning normally.' +
                                       ' See below for details.';

      // Change the icon to a check mark.
      this.$.statusIcon.src = gbActionPanelItem.ICON_URLS['normal'];
      break;
  }
};

/** Controls whether a warning about the MCU status is visible on the panel.
 * @private
 * @param state The current Redux state.
 */
gbActionPanel.updateMCUAlive_ = function*(state) {
  // The action panel message.
  const message = gbActionPanelMessages.mcuNotResponding;

  let action = null;
  const alive = state.fromBackend.mcu_alive;
  if (alive && message.id in state.actionPanel.items) {
    // Remove the message.
    action = actions.removePanelItem(message.id);
  } else if (!alive && !(message.id in state.actionPanel.items)) {
    // Add the message.
    action = actions.addPanelItem(message.title, message.description,
                                  message.level, message.id);
  }

  if (action != null) {
    // Dispatch the action if we need to.
    yield ReduxSaga.effects.put(action);
  }
};

/** Controls messages related to module status.
 * @private
 * @param state The current Redux state.
 */
gbActionPanel.updateModules_ = function*(state) {
  if (!state.fromBackend.mcu_alive) {
    // If the MCU is dead, we're not in communication with the modules anyway,
    // so there's not much we can do here.
    return;
  }

  // The message about having no modules.
  const message = gbActionPanelMessages.noModules;

  let action = null;
  const noModules = (Object.keys(state.fromBackend.modules).length === 0);
  if (!noModules && message.id in state.actionPanel.items) {
    // Remove the message.
    action = actions.removePanelItem(message.id);
  } else if (noModules && !(message.id in state.actionPanel.items)) {
    // Add the message.
    action = actions.addPanelItem(message.title, message.description,
                                  message.level, message.id);
  }

  if (action != null) {
    // Dispatch the action if we need to.
    yield ReduxSaga.effects.put(action);
  }
};

// Sub-namespace specifically for saga handlers.
gbActionPanel.sagas = {};

/** Saga that handles adding an item to the action panel when the ADD_PANEL_ITEM
 * action is fired.
 * @private
 * @param action The specific action specifying the item to add.
 */
gbActionPanel.sagas.addSaga_ = function*(action) {
  let store = main.getReduxStore();
  const state = store.getState();

  // Get the panel from the state.
  let panel = state.actionPanel.actionPanel;
  if (!panel) {
    throw new ReferenceError('actionPanel not set in Redux state!');
  }

  // Add the actual item to the DOM.
  let node = panel.addItem(action.title, action.description, action.level);

  // Update the summary panel.
  panel.updatePanelTop(state.actionPanel);

  // All that's left to do is save the actual node. We delegate back to the
  // reducers for this.
  yield ReduxSaga.effects.put(actions.updatePanelItemList(action.id, node));
};

/** Saga that handles removing an item from the action panel when the
 * REMOVE_PANEL_ITEM action is fired.
 * @private
 * @param action The action specifying the item to remove.
 */
gbActionPanel.sagas.removeSaga_ = function*(action) {
  let store = main.getReduxStore();
  const state = store.getState();

  // Get the panel from the state.
  let panel = state.actionPanel.actionPanel;
  if (!panel) {
    throw new ReferenceError('actionPanel not set in Redux state!');
  }

  // Find the item to remove.
  let to_remove = state.actionPanel.items[action.id];
  // Remove it.
  panel.removeItem(to_remove);

  // Update the summary panel.
  panel.updatePanelTop(state.actionPanel);

  // Remove the node in the state.
  yield ReduxSaga.effects.put(actions.updatePanelItemList(action.id, null));
};

/** Saga that handles updating the action panel when the backend state changes.
 * @private
 * @param action The action specifying the state update.
 */
gbActionPanel.sagas.updateBackendStateSaga_ = function*(action) {
  let store = main.getReduxStore();
  const state = store.getState();

  // Get the panel from the state.
  let panel = state.actionPanel.actionPanel;
  if (!panel) {
    throw new ReferenceError('actionPanel not set in Redux state!');
  }

  // Check if any update happened that we need to care about.
  if (!utilities.areDisjoint(['mcu_alive'], action.key)) {
    // The MCU aliveness status might have changed. We probably need to either
    // add or remove a message.
    yield *gbActionPanel.updateMCUAlive_(state);
  }

  if (!utilities.areDisjoint(['modules'], action.key)) {
    // One of our modules changed in some way. We might have to show a message
    // about it.
    yield *gbActionPanel.updateModules_(state);
  }
};

/** Listens for ADD_PANEL_ITEM events and dispatches Sagas to handle them.
 * @private
 */
gbActionPanel.sagas.addSagaWaiter_ = function*() {
  yield *ReduxSaga.takeLatest(actions.ADD_PANEL_ITEM,
                              gbActionPanel.sagas.addSaga_);
};

/** Listens for REMOVE_PANEL_ITEM events and dispatches Sagas to handle them.
 * @private
 */
gbActionPanel.sagas.removeSagaWaiter_ = function*() {
  yield *ReduxSaga.takeLatest(actions.REMOVE_PANEL_ITEM,
                              gbActionPanel.sagas.removeSaga_);
};

/** Listens for UPDATE_BACKEND_STATE events and dispatches Sagas to handle them.
 * @private
 */
gbActionPanel.sagas.updateBackendStateSagaWaiter_ = function*() {
  yield *ReduxSaga.takeLatest(actions.UPDATE_BACKEND_STATE,
                              gbActionPanel.sagas.updateBackendStateSaga_);
};
