// Namespace for this file.
gbGrowingProgress = {};

/** Creates the element. */
gbGrowingProgress.create = function() {
  console.log('Creating growing progress panel.');

  Polymer({
    is: 'gb-growing-progress',
    ready: gbGrowingProgress.ready_,

    addItem: gbGrowingProgress.addItem_,
    addEmptyItem: gbGrowingProgress.addEmptyItem_,
    removeItem: gbGrowingProgress.removeItem_,
  });
};

/** Runs on creation for the growing progress panel.
 * @private
 */
gbGrowingProgress.ready_ = function() {
  // Start running sagas.
  let saga = main.getSagaMiddleware();
  saga.run(gbGrowingProgress.sagas.updateBackendStateSagaWaiter_);

  // Register the instance.
  let store = main.getReduxStore();
  store.dispatch(actions.setGrowingProgress(this));
};

/** Adds a new item without setting attributes. The item will be the default
 *  empty module entry.
 * @private
 * @return The DOM node of the added item.
 */
gbGrowingProgress.addEmptyItem_ = function() {
  // First, create a new child item.
  let item = document.createElement('gb-growing-progress-item');

  // Remove the default empty panel message.
  let emptyMessage = this.$.emptyMessage;
  if (emptyMessage.style.display != 'none') {
    emptyMessage.style.display = 'none';
  }

  // Insert the item.
  Polymer.dom(this).appendChild(item);

  return item;
};

/** Adds a new item to the growing progress panel.
 * @private
 * @param name The name of the plant.
 * @param daysTotal The total number of days the plant must grow for.
 * @param daysElapsed The number of days that the plant has been growing for.
 * @param icon The url of the icon to use for the plant.
 * @return The DOM node of the added item.
 */
gbGrowingProgress.addItem_ = function(name, daysTotal, daysElapsed, icon) {
  let item = this.addEmptyItem();

  // Configure the item.
  item.setName(name);
  item.setTotalDays(daysTotal);
  item.setElapsedDays(daysElapsed);
  item.setIcon(icon);

  return item;
};

/** Removes an item from the growing progress panel.
 * @private
 * @param permanentID The permanent ID of the module corresponding to that item.
 */
gbGrowingProgress.removeItem_ = function(permanentID) {
  // Get the item node.
  let store = main.getReduxStore();
  const state = store.getState();

  let item = state.growingProgress.items[permanentID];

  // Remove it. Polymer doesn't really have an API to remove an element
  // directly, which is why this is so involved.
  let myParent = Polymer.dom(item).parentNode;
  Polymer.dom(myParent).removeChild(item);
}

/** Updates the panel based on the current module list in the state.
 * @private
 * @param state The current state.
 */
gbGrowingProgress.updateModules_ = function*(state) {
  // Check for anything we need to remove from the panel.
  for (permanentID in state.growingProgress.items) {
    if (!(permanentID in state.fromBackend.modules)) {
      // This module went away, so remove it.
      let element = state.growingProgress.growingProgress;
      element.removeItem(permanentID);

      // Remove the item from the state.
      const action = actions.updateGrowingProgressItemList(permanentID, null);
      yield ReduxSaga.effects.put(action);
    }
  }

  // Check for anything we need to add or update.
  for (permanentID in state.fromBackend.modules) {
    const module = state.fromBackend.modules[permanentID];

    const name = module.name;
    const daysTotal = module.timing.grow_days;
    const daysElapsed = module.timing.grow_days_elapsed;
    const icon = module.icon_url;

    if (!(permanentID in state.growingProgress.items)) {
      // We don't have a listing for this module yet.
      let element = state.growingProgress.growingProgress;
      let item = null;
      if (!name) {
        // A special case is the default empty module.
        item = element.addEmptyItem();
      } else {
        // Non-empty module.
        item = element.addItem(name, daysTotal, daysElapsed, icon);
      }

      // Save the new item to the state.
      const action = actions.updateGrowingProgressItemList(permanentID, item);
      yield ReduxSaga.effects.put(action);

    } else {
      // If the item is already represented, we just have to update it.
      let item = state.growingProgress.items[permanentID];

      item.setName(name);
      item.setTotalDays(daysTotal);
      item.setElapsedDays(daysElapsed);
      item.setIcon(icon);
    }
  }
};

// Sub-namespace specifically for saga handlers.
gbGrowingProgress.sagas = {};

/** Saga that handles updating the growing progress panel when the backend state
 * changes.
 * @private
 * @param action The action specifying the state update.
 */
gbGrowingProgress.sagas.updateBackendStateSaga_ = function*(action) {
  let store = main.getReduxStore();
  const state = store.getState();

  // Get the panel from the state.
  let panel = state.growingProgress.growingProgress;
  if (!panel) {
    throw new ReferenceError('growingProgress panel not set in Redux state!');
  }

  if (!utilities.areDisjoint(['modules'], action.key)) {
    // If we modified the modules list, we might have to update the panel.
    yield *gbGrowingProgress.updateModules_(state);
  }
};

/** Listens for UPDATE_BACKEND_STATE events and dispatches Sagas to handle them.
 * @private
 */
gbGrowingProgress.sagas.updateBackendStateSagaWaiter_ = function*() {
  yield *ReduxSaga.takeLatest(actions.UPDATE_BACKEND_STATE,
                              gbGrowingProgress.sagas.updateBackendStateSaga_);
};
