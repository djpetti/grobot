// Namespace for this file.
gbErrorModal = {};

/** @private
 * Creates the element. */
gbErrorModal.create = function() {
  Polymer({
    is: 'gb-error-modal',
    behaviors: [main.getReduxBehavior()],
    properties: {
      allGood: {
        type: Boolean,
        value: false,
        observer: 'allGoodChanged_',
        statePath: 'fromBackend.mcuAlive',
      }
    },

    /** Observer for the allGood property, which is set to false when the MCU
     * stops responding.
     * @private
     * @param newValue The new value of the parameter.
     * @param oldValue The old value of the parameter. */
    allGoodChanged_: function(newValue, oldValue) {
      // We want to show this when the MCU is not responding.
      this.$.errorDialog.opened = !newValue;
    },
  });
};

gbErrorModal.create();
