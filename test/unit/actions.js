define([
  'intern!object',
  'intern/chai!assert',
  'app/actions.js'
], function (registerSuite, assert) {
  registerSuite({
    name: 'actionsTest',

    /** Tests that an unknown action does not result in a state change.
     */
    noDefaultStateChange: function() {
      // Empty action.
      const state = actions.initialState;
      let new_state = actions.grobotAppReducer(state, 'BAD_ACTION');
      // The state shouldn't be copied, so this will be a strictEqual.
      assert.strictEqual(state, new_state);
    },

    /** Test that the UPDATE_BACKEND_STATE action works as expected. */
    backendState: function() {
      // Create an initial state to start with.
      const state = actions.initialState;
      assert.isFalse(state.errorModalOpened);

      // Now, create an action that should not change the state.
      const alive_backend_state = {mcu_alive: true};
      const alive_action = actions.updateBackendState(alive_backend_state);

      // The state should remain the same.
      let new_state = actions.grobotAppReducer(state, alive_action);
      assert.deepEqual(state, new_state);

      // Now, create an action that changes the state.
      const dead_backend_state = {mcu_alive: false};
      const dead_action = actions.updateBackendState(dead_backend_state);

      // The state should change.
      new_state = actions.grobotAppReducer(state, dead_action);
      assert.notDeepEqual(state, new_state);
      assert.isTrue(new_state.errorModalOpened);

      // Change it back.
      new_state = actions.grobotAppReducer(new_state, alive_action);
      assert.deepEqual(state, new_state);
    }
  });
});
