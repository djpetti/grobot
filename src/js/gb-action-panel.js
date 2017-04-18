// Namespace for this file.
gbActionPanel = {};

/** @private
 * Creates the element. */
gbActionPanel.create = function() {
  Polymer({
    is: 'gb-action-panel',
    ready: gbActionPanel.ready_,

    addItem: gbActionPanel.addItem_,
    updatePanelTop: gbActionPanel.updatePanelTop_,
  });
};

/** Runs on creation for the action panel.
 * @private
 */
gbActionPanel.ready_ = function() {
  // Dispatch the proper polymer action.
  let store = main.getReduxStore();
  store.dispatch(actions.setActionPanel(this));
}

/** Adds a new item to the action panel.
 * @private
 * @param title The title of the item.
 * @param description The description of the item.
 * @param level The level of the item. Must by a string in
 *              "normal", "warning", or "error".
 * @returns The DOM node of the added item.
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

      if (errorLength === 0) {
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
}
