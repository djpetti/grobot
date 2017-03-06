#!/usr/bin/python3


import argparse
import os
import subprocess
import sys
import unittest

from backend import server


""" Script to manage building and testing the web application. """


def build_polymer_app():
  # Get directory that the script it in.
  script_path = os.path.dirname(os.path.realpath(__file__))

  if subprocess.call(["polymer", "build"], cwd=script_path):
    print("ERROR: Polymer build failed!")
    sys.exit(1)

  # TODO (danielp): Figure out why polymer doesn't want to run sw-precache.
  config_path = os.path.join(script_path, "sw-precache-config.js")
  if subprocess.call(["sw-precache", "--config", config_path], cwd=script_path):
    print("ERROR: Generating service worker failed!")
    sys.exit(1)
  # Move the generated file to the right place.
  service_worker_file = os.path.join(script_path, "service-worker.js")
  built_service_worker = os.path.join(script_path,
                                      "build/bundled/service-worker.js")
  os.rename(service_worker_file, built_service_worker)

def run_all_tests():
  """ Runs all the tests.
  Returns:
    True if the tests all succeed, False if there are failures. """
  print("Starting tests...")

  loader = unittest.TestLoader()
  # Get the directory this module is in.
  dir_path = os.path.dirname(os.path.realpath(__file__))
  suite = loader.discover("backend/tests", top_level_dir=dir_path)

  test_result = unittest.TextTestRunner(verbosity=2).run(suite)
  if not test_result.wasSuccessful():
    return False

  return True


def main():
  parser = argparse.ArgumentParser( \
      description="Run and test the web application.")
  parser.add_argument("-p", "--production", action="store_true",
                      help="Rebuild polymer app and serve from build/bundled.")
  parser.add_argument("-t", "--test-only", action="store_true",
                      help="Only run the tests and nothing else.")
  args = parser.parse_args()

  # Build the polymer app.
  if args.production:
    print("Building polymer app...")
    build_polymer_app()

  # Run the tests.
  if not run_all_tests():
    print("ERROR: Tests failed, not continuing.")
    sys.exit(1)

  # Run the dev server.
  if not args.test_only:
    print("Starting dev server...")
    server.main(dev_mode=(not args.production))


if __name__ == "__main__":
  main()
