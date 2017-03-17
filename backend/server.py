#!/usr/bin/python3


import json
import logging
import os
import sys

import tornado.ioloop
import tornado.web

from . import cron
from . import serial_talker
from . import websocket


""" Runs a tornado web server. This is the main backend for the GroBot system.
"""


def _configure_logging():
  """ Configure logging handlers. """
  # Configure root logger.
  root = logging.getLogger()
  root.setLevel(logging.DEBUG)
  file_handler = logging.FileHandler("grobot_server.log")
  file_handler.setLevel(logging.DEBUG)
  stream_handler = logging.StreamHandler()
  stream_handler.setLevel(logging.INFO)
  formatter = logging.Formatter("%(name)s@%(asctime)s: " +
      "[%(levelname)s] %(message)s")
  file_handler.setFormatter(formatter)
  stream_handler.setFormatter(formatter)
  root.addHandler(file_handler)
  root.addHandler(stream_handler)

# Initialize logging system.
_configure_logging()
logger = logging.getLogger(__name__)


def make_app(settings, dev_mode=False):
  """ Creates the tornado application.
  Args:
    settings: The settings loaded from the settings file.
    dev_mode: If set to True, will serve data from the base directory instead of
              the build directory. This is useful for testing.
  Returns:
    The built and configured app. """
  base_path = "build/bundled"
  if dev_mode:
    base_path = ""
  bower_path = {"path": os.path.join(base_path, "bower_components")}
  image_path = {"path": os.path.join(base_path, "images")}
  template_path = settings.get("template_path", "src")
  template_path = {"path": os.path.join(base_path, template_path)}
  root_path = {"path": base_path,
               "default_filename": "index.html"}

  # Create and run the application.
  app = tornado.web.Application([
      # Specific configuration for static files that need to be available for
      # polymer.
      (r"/bower_components/(.*)", tornado.web.StaticFileHandler, bower_path),
      (r"/images/(.*)", tornado.web.StaticFileHandler, image_path),
      (r"/src/(.*)", tornado.web.StaticFileHandler, template_path),
      (r"/(service-worker\.js)", tornado.web.StaticFileHandler, root_path),
      (r"/(manifest\.json)", tornado.web.StaticFileHandler, root_path),
      (r"/(app_socket)", websocket.GrobotWebSocket),
      (r"/(.*)", tornado.web.StaticFileHandler, root_path)],
      **settings)

  return app

def make_serial(settings):
  """ Initializes the serial subsystem.
  Args:
    settings: The settings loaded from the settings file.
  Returns:
    The configured SerialTalker. """
  device = settings.get("mcu_serial", "/dev/ttyS0")
  baudrate = settings.get("mcu_baudrate", 19200)
  serial = None
  try:
    serial = serial_talker.SerialTalker(baudrate, device=device)
  except ValueError:
    # Serial initialization failed. (Already logged.) We're going to keep
    # running the server to the best of our ability so that we can at least
    # notify the user.
    pass

  return serial


def main(dev_mode=False):
  """ Runs the main server event loop.
  Args:
    dev_mode: If set to True, it will serve data from the base directory instead
              of from the build directory. This is useful if we want to debug
              stuff locally without running 'polymer build.'"""
  # Load the settings initially.
  try:
    settings_file = open("backend_settings.json")
  except OSError:
    logger.critical("Cannot find 'backend_settings.json'. Aborting.")
    sys.exit(1)

  settings = json.load(settings_file)
  settings_file.close()
  logger.info("Loaded settings.")

  app = make_app(settings, dev_mode=dev_mode)
  # Initialize serial subsystem.
  serial = make_serial(settings)

  # Start listening.
  port = settings.get("listen_port")
  if not port:
    logger.critical("Expected 'port' in settings.")
    sys.exit(1)
  port = int(port)
  logger.info("Listening on port %d." % (port))
  app.listen(port)

  # Start periodic jobs.
  if serial:
    cron.CheckMcuAliveJob(10000, serial)

  logger.info("Starting server...")
  tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
  main()
