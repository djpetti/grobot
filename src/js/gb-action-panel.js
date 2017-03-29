// Namespace for this file.
gbActionPanel = {};

/** @private
 * Creates the element. */
gbActionPanel.create = function() {
  Polymer({
    is: 'gb-action-panel',
    behaviors: [main.getReduxBehavior()],
  });
};

gbActionPanel.create();
