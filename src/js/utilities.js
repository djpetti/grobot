// Namespace for miscellaneous utility functions.
utilities = {};

/** Helper function that determines whether a particular key in the state is a
 *  sub-key of another one.
 * @param key The key to check.
 * @param superKey The posible superkey.
 * @return True if key is a subkey of superKey, false otherwise.
 */
utilities.isSubkey = function(key, superKey) {
  if (superKey.length > key.length) {
    // Superkey is more specific, so this can't possibly be true.
    return false;
  }

  for (i = 0; i < superKey.length; ++i) {
    if (superKey[i] != key[i]) {
      // They don't match at this level.
      return false;
    }
  }

  // Everything appears to match.
  return true;
};

/** Determines whether two keys are disjoint. Keys are disjoint if neither is a
 * sub-key of the other. */
utilities.areDisjoint = function(key1, key2) {
  return !(utilities.isSubkey(key1, key2) || utilities.isSubkey(key2, key1));
};
