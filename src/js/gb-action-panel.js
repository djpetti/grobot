// Namespace for this file.
gbActionPanel = {};

/** @private
 * Creates the element. */
gbActionPanel.create = function() {
  Polymer({
    is: 'gb-action-panel',
    ready: function() {
      return gbActionPanel.ready_(this);
    },

    addItem: function(title, description, level) {
      return gbActionPanel.addItem_(this, title, description, level);
    },
  });
};

/** Runs on creation for the action panel.
 * @private
 * @param element The element we are operating on.
 */
gbActionPanel.ready_ = function(element) {
  // Dispatch the proper polymer action.
  let store = main.getReduxStore();
  store.dispatch(actions.setActionPanel(element));
}

/** Adds a new item to the action panel.
 * @private
 * @param element The element we are operating on.
 * @param title The title of the item.
 * @param description The description of the item.
 * @param level The level of the item. Must by a string in
 *              "normal", "warning", or "error".
 * @returns The DOM node of the added item.
 */
gbActionPanel.addItem_ = function(element, title, description, level) {
  // First, create a new child item.
  let item = document.createElement('gb-action-panel-item');

  // Configure the item.
  item.setTitle(title);
  item.setDescription(description);
  item.setLevel(level);

  // Add the child node.
  Polymer.dom(element).appendChild(item);

  return item;
};
