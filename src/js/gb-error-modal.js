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
        observer: 'openedChanged_',
        statePath: 'fromBackend.errorModalOpened',
      }
    },

    openedChanged_: function(newValue, oldValue) {
      this.$.errorDialog.opened = newValue;
    },
  });
};

gbErrorModal.create();
