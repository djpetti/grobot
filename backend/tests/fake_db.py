import logging

from bson.objectid import ObjectId

from pymongo import ReturnDocument

import tornado.concurrent


""" Utilities for simulating a database, meant for testing purposes. """


logger = logging.getLogger(__name__)


class FakeDatabase:
  """ Simulates a database. """

  def __init__(self):
    # Collections currently in the database.
    self.__collections = {}

  def __get_collection(self, name):
    """ Gets a collection, or creates a new one if it does not exist.
    Args:
      name: The name of the collection.
    Returns:
      The collection requested. """
    if name not in self.__collections:
      logger.info("Creating new fake collection '%s'." % (name))
      self.__collections[name] = FakeCollection(name)

    return self.__collections[name]

  def clear(self):
    """ Purges the database of all data. """
    self.__colections = {}

  def __getattr__(self, attribute):
    """ This replicates the actual Motor interface, in which this syntax is used
    to get a collection. """
    return self.__get_collection(attribute)

  def __getitem__(self, item):
    """ This also replicates a Motor interface. Using the dictionary syntax is
    another way to get a collection. """
    return self.__get_collection(item)


class FakeCollection:
  """ Simulates a collection. """

  def __init__(self, name):
    """
    Args:
      name: The name of the collection. """
    self.__name = name

    # Stores the actual data.
    self.__documents = []
    # Associated unit test instance.
    self.__test_instance = None

  def __return_future(self, value):
    """ Helper that creates an immediately-read future returning value.
    Args:
      value: The value to return.
    Returns:
      A future encapsulating value. """
    future = tornado.concurrent.Future()
    future.set_result(value)

    return self.__return_with_test_stop(future)

  def __callback_or_return(self, callback, value):
    """ Helper that either runs a callback or returns a value. If callback is
    None, it will return the value, otherwise it will run callback, passing the
    value as the first argument, and None for the error.
    Args:
      callback: The callback to (maybe) run.
      value: The value to return or pass.
    Returns:
      value if the callback was not used, None if it was. """
    if callback:
      # Run the callback.
      callback(value, None)
      return self.__return_future(None)

    return self.__return_future(value)

  def __return_with_test_stop(self, value):
    """ Returns a value and stops the test if needed.
    Args:
      value: The value to return.
    Returns:
      The value passed in. """
    if self.__test_instance:
      # Stop the test.
      self.__test_instance.stop()

    return value

  def __create_document(self):
    """ Helper that creates a new document with a random ObjectId.
    Returns:
      The new created document. """
    # Make the object ID.
    object_id = ObjectId()
    return {"_id": object_id}

  def __find_one(self, db_filter):
    """ Looks for an object in the collection that matches a filter.
    Args:
      db_filter: The filter to match.
    Returns:
      The document it found, or None if it found nothing. """
    # Scan for the object.
    logger.debug("Searching for %s in %s." % (db_filter, self.__documents))

    for document in self.__documents:
      for key in db_filter.keys():
        if key not in document:
          break
        if db_filter[key] != document[key]:
          break

      else:
        # We found a match.
        logger.debug("Found matching document: %s" % (document))
        return document

    return None

  def __set_in_document(self, document, update):
    """ Uses the contents up an update dictionary to change the collection.
    Args:
      document: The document to update.
      update: A dictionary. For each key, the equivalent key in the document
              will be set to that value. """
    for key, value in update.items():
      document[key] = value

  def find_one(self, db_filter=None, callback=None):
    """ Behaves like the Motor function find_one. Note that this version doesn't
    support as many additional arguments as Motor does. """
    document = self.__find_one(db_filter)
    return self.__callback_or_return(callback, document)

  def find_one_and_update(self, db_filter, update, **kwargs):
    """ Behaves like the similarly-named Motor function. Note that this version
    doesn't support as many additional arguments as Motor does. """
    # Insert it if it's not there.
    upsert = kwargs.pop("upsert", False)
    # Return the new document instead of the old one.
    return_document = kwargs.pop("return_document", ReturnDocument.BEFORE)
    # Possible callback.
    callback = kwargs.pop("callback", None)

    if len(kwargs):
      raise ValueError("Unknown keyword arguments: %s" % (kwargs))

    # First, try to find the document we want.
    document = self.__find_one(db_filter)
    if not document:
      # The document is not here.
      logger.debug("No document found for update.")
      if not upsert:
        # This is a failure condition.
        return self.__callback_or_return(callback, None)

      # Otherwise, continue, but build from a new, empty, document.
      document = self.__create_document()

    old_document = document.copy()

    # Set of currently-supported updates. More may be added.
    supported_updates = set(["$set"])
    for key in update.keys():
      # Check that they're supported.
      if key not in supported_updates:
        raise ValueError("Unsupported update type: '%s'" % (key))

    # Perform whatever updates we need to.
    for key, value in update.items():
      if key == "$set":
        # Set the new value in the document.
        # The value is itself a dictionary indicating what we want to set.
        self.__set_in_document(document, value)

    # Add it to the collection.
    self.__documents.append(document)

    to_return = old_document
    if return_document == ReturnDocument.AFTER:
      # Return the changed document instead of the original.
      to_return = document

    logger.debug("Update: old doc: %s, new doc: %s" % (old_document, document))

    return self.__callback_or_return(callback, to_return)

  def add_document(self, document):
    """ Adds a document manually to the collection. An ObjectId will
    automatically be set. Meant to be used for testing.
    Args:
      document: The document to add. """
    # We'll handle the ID by creating a new document, and merging in the
    # specified one.
    new_document = self.__create_document()
    self.__set_in_document(new_document, document)

    logger.debug("Manually adding document: %s" % (new_document))
    self.__documents.append(new_document)

  def get_documents(self):
    """ Gets all the documents in the collection. Meant to be used for testing.
    Returns:
      All the documents. """
    return self.__documents

  def enable_test_stop(self, test_instance):
    """ Enables calling stop() for a unit test after every database operation.
    Args:
      test_instance: The instance to call stop() on. """
    self.__test_instance = test_instance

  def disable_test_stop(self):
    """ Disables calling stop() for a unit test after every database operation.
    """
    self.__test_instance = None
