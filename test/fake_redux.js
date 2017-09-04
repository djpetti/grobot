/** Including this file in an script tag defines a fake Redux state for testing
 * that overrides the real one. */

// Namespace for this file.
fakeRedux = {};

/** Fake Redux store for testing. */
fakeRedux.store = class {
  constructor() {
    // Fake state for testing. The deep cloning method is terribly inneficient,
    // but for testing, correctness matters more than speed.
    this.state_ = JSON.parse(JSON.stringify(actions.initialState));
    // Any actions dispatched to the fake store.
    this.dispatchedActions_ = [];
  }

  /** Gets the fake Redux state.
   * @returns The fake Redux state. */
  getState() {
    return this.state_;
  }

  /** Gets the currently dispatched actions.
   @returns The actions that were dispatched. */
  getDispatchedActions() {
    return this.dispatchedActions_;
  }

  /** Sets the fake Redux state.
   * @param state The new state to set. */
  setState(state) {
    this.state_ = state;
  }

  /** Save actions, so we can verify that they happen, but don't change the
   * state. (We'll do that manually.)
   * @param action The action that we are dispatching. */
  dispatch(action) {
    this.dispatchedActions_.push(action);
  }

  /** Initializes a new fake store and replaces the handles to the actual store
   * with it. */
  static initFakeState() {
    let store = new fakeRedux.store();

    // Override the real one.
    main.getReduxStore = function() {
      return store;
    };
  }
};
