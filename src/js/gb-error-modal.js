// Namespace for this file.
gbErrorModal = {};

/** @private
 * Creates the element. */
gbErrorModal.create = function() {
  Polymer({
    is: 'gb-error-modal',
    behaviors: [main.getReduxBehavior()],
    properties: {
      opened: {
        type: Boolean,
        value: false,
        observer: '_openedChanged',
        statePath: 'errorModalOpened',
      }
    },

    _openedChanged: function(newValue, oldValue) {
      this.$.errorDialog.opened = newValue;
    },
  });
};

gbErrorModal.create();
